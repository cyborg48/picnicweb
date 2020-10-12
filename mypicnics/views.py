from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Picnic, Membership, Artwork, Feedback, Img
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import random
from users.models import PicnicUser, Notification
from .forms import PicnicJoinForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
import json

# Create your views here.
def home(request): 
    context = {
        'full': True,
        'title':'Picnic',
    }
    return render(request, 'mypicnics/home.html', context)

def changelog(request): 
    context = {
        'small': True,
        'title':'Changelog',
    }
    return render(request, 'mypicnics/changelog.html', context)

class PicnicCreateView(LoginRequiredMixin, CreateView):
    model = Picnic
    success_url='/my-picnics'
    # template_name = 'mypicnics/form.html'
    fields = ['name', 'background_image', 'description']

    def get_context_data(self, **kwargs):
        context = super(PicnicCreateView, self).get_context_data(**kwargs)
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.host = self.request.user
        form.instance.key = generateKey()
        form.instance.background_image = form.cleaned_data['background_image']
        return super().form_valid(form)

class PicnicDetailView(LoginRequiredMixin, DetailView):
    model = Picnic

    def get_context_data(self, **kwargs):
        context = super(PicnicDetailView, self).get_context_data(**kwargs)
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        picnic = Picnic.objects.get(id=self.kwargs['pk'])
        context['member'] = Membership.objects.get(group=picnic, member=self.request.user)
        return context

    def get_object(self, queryset=None):
        pUser = PicnicUser.objects.get(user=self.request.user)
        obj = super(PicnicDetailView, self).get_object(queryset=pUser.picnics)
        if obj == None:
            raise Http404()
        print(obj.background_image.url)
        return obj

@login_required
def myPicnics(request):
    currUser = PicnicUser.objects.get(user=request.user)
    context = {
        'small': True,
        'title':'My Picnics',
        'pUser':currUser
    }
    return render(request, 'mypicnics/mypicnics.html', context)

def generateKey():
    randomKey = ""
    possibleValues = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for x in range(6):
        randomKey = randomKey + str(possibleValues[random.randint(0, len(possibleValues)-1)])
    for picnic in Picnic.objects.all():
        if picnic.key == randomKey:
            randomKey = generateKey
    return randomKey

@login_required
def joinPicnic(request):

    if request.method == 'POST':
        form = PicnicJoinForm(request.POST)
        if form.is_valid():
            # form.save()
            key = form.cleaned_data.get('key')
            picnic_exists = False
            for picnic in Picnic.objects.all():
                if picnic.key == key:
                    picnic_exists = True
                    is_member = False
                    for membership in picnic.members.all():
                        if membership == request.user:
                            is_member = True
                    if not is_member:
                        print(len(picnic.members.all()))
                        if len(picnic.members.all()) < 15:
                            m = Membership(group=picnic, member=request.user, nickname=request.user.username)
                            m.save()
                            # picnic.members.add(m)
                            PicnicUser.objects.get(user=request.user).picnics.add(picnic)
                            n = Notification(message=request.user.username + " has joined your Picnic \"" + picnic.name + ".\"", \
                                picnicid=picnic.id)
                            n.save()
                            pUser = PicnicUser.objects.get(user=picnic.host)
                            pUser.notifs.add(n)
                            pUser.hasNotifications = True
                            pUser.save()
                            messages.success(request, f'You have successfully joined this Picnic!')
                            return redirect('my-picnics')
                        else: 
                            messages.warning(request, f'This Picnic is already full! Maximum of 15 people per Picnic.')
                            return redirect('my-picnics')
                    else:
                        messages.warning(request, f'You have already joined this Picnic!')
                        return redirect('my-picnics')
            if not picnic_exists:
                messages.warning(request, f'A picnic with that invite code does not exist!')
                return redirect('my-picnics')
            # username = form.cleaned_data.get('username')
            # messages.success(request, f'Your account has been created! You are now able to log in.')
            # return redirect('mypicnics')
    else:
        form  = PicnicJoinForm()
    context = {
        'small': True,
        'title':'My Picnics',
        'modal':True,
        'form':form,
    }
    return render(request, 'mypicnics/mypicnics.html', context)

class ArtworkCreateView(LoginRequiredMixin, CreateView):
    model = Artwork
    # template_name="mypicnics/picnic_detail.html"
    fields = ['title', 'description', 'feedback']
    success_url='/picnic/'
    

    def get_context_data(self, **kwargs):
        self.success_url += str(self.kwargs['pk'])
        context = super(ArtworkCreateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['pk']
        context['object'] = Picnic.objects.get(id=self.kwargs['pk'])
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        picnic = Picnic.objects.get(id=self.kwargs['pk'])
        context['member'] = Membership.objects.get(group=picnic, member=self.request.user)
        return context

    def form_valid(self, form):
        picnic = Picnic.objects.get(pk=self.kwargs['pk'])
        self.success_url += str(self.kwargs['pk'])
        form.instance.artist = self.request.user
        form.instance.group = picnic
        # form.instance.artwork = request.FILES['artwork']
        form.save()
        count = 0
        for file in self.request.FILES.getlist('images'):
            image = Img.objects.create(
                img=file
            )
            image.save()
            if count == 0:
                form.instance.cover = image
            count += 1
            form.instance.artwork.add(image)
        # instance.save()
        form.save()
        picnic.artworks.add(form.instance)
        membership = Membership.objects.filter(member=self.request.user, group=picnic)[0]
        membership.num_uploads += 1
        membership.save()
        return super().form_valid(form)

class ArtworkDetailView(LoginRequiredMixin, DetailView):
    model = Artwork
    context_object_name = "art"

    def get_context_data(self, **kwargs):
        context = super(ArtworkDetailView, self).get_context_data(**kwargs)
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['picnicID'] = self.kwargs['picnicid']
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context
    
    def get_object(self, queryset=None):
        pUser = PicnicUser.objects.get(user=self.request.user)
        obj = super(ArtworkDetailView, self).get_object(queryset=pUser.picnics.get(id=self.kwargs['picnicid']).artworks)
        if obj == None:
            raise Http404()
        return obj

class CritiqueCreateView(LoginRequiredMixin, CreateView):
    model = Feedback
    fields = ['bread1', 'middle', 'bread2']
    success_url='/picnic/'

    def get_context_data(self, **kwargs):
        self.success_url += str(self.kwargs['picnicid']) + '/artwork/' + str(self.kwargs['artworkid'])
        context = super(CritiqueCreateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['artworkid']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['art'] = Artwork.objects.get(id=self.kwargs['artworkid'])
        context['picnicID'] = self.kwargs['picnicid']
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        artwork = Artwork.objects.get(pk=self.kwargs['artworkid'])
        self.success_url += str(self.kwargs['picnicid']) + "/artwork/" + str(self.kwargs['artworkid'])
        form.instance.critiquer = self.request.user
        form.save()
        artwork.critiques.add(form.instance)
        membership = Membership.objects.filter(member=self.request.user, group=Picnic.objects.get(id=self.kwargs['picnicid']))[0]
        membership.num_critiques += 1
        membership.save()
        n = Notification(message=self.request.user.username + " has critiqued your piece \"" + artwork.title + ".\"", \
            picnicid=self.kwargs['picnicid'], artworkid=self.kwargs['artworkid'])
        n.save()
        pUser = PicnicUser.objects.get(user=artwork.artist)
        pUser.notifs.add(n)
        pUser.hasNotifications = True
        pUser.save()
        return super().form_valid(form)

class PicnicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Picnic
    success_url='/my-picnics/'
    template_name = 'mypicnics/picnic_update.html'
    fields = ['name', 'background_image', 'description']

    def get_context_data(self, **kwargs):
        self.success_url += str(self.kwargs['pk'])
        context = super(PicnicUpdateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['pk']
        context['object'] = Picnic.objects.get(id=self.kwargs['pk'])
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        form.instance.host = self.request.user
        # form.instance.key = generateKey()
        form.instance.background_image = form.cleaned_data['background_image']
        return super().form_valid(form)

    def test_func(self):
        picnic = self.get_object()
        if self.request.user == picnic.host:
            return True
        return False

@login_required
def leavePicnic(request, pk, userid):

    if request.method == 'POST':
        user = User.objects.get(id=userid)
        picnicuser = PicnicUser.objects.get(user=user)
        picnic = Picnic.objects.get(id=pk)
        if userid == request.user.id:
            if picnic.host == user:
                Picnic.objects.filter(id=pk).delete()
            else:
                picnic.members.remove(user)
                picnicuser.picnics.remove(picnic)
                print("Bye")
            messages.success(request, f'You have successfully left this Picnic!')
            return redirect('my-picnics')
        else:
            picnic.members.remove(user)
            picnicuser.picnics.remove(picnic)
            print("u just got le boot")
            messages.success(request, user.username + " has been removed from this Picnic.")
            return redirect('picnic-detail', pk=pk)
    context = {
        'object': Picnic.objects.get(id=pk),
        'leave': userid == request.user.id,
        'username': User.objects.get(id=userid).username,
        'pUser':PicnicUser.objects.get(user=request.user)
    }
    return render(request, 'mypicnics/leavepicnic.html', context)

class ArtDelete(LoginRequiredMixin, DeleteView):
    model = Artwork

    def get_context_data(self, **kwargs):
        self.picnicid = self.kwargs['picnicid']
        context = super(ArtDelete, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['pk']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['art'] = Artwork.objects.get(id=self.kwargs['pk'])
        context['picnicID'] = self.kwargs['picnicid']
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Artwork successfully deleted.")
        return reverse_lazy('picnic-detail', kwargs={'pk': self.kwargs['picnicid']})
    
    def form_valid(self, form):
        return super().form_valid(form)

class CritiqueDelete(LoginRequiredMixin, DeleteView):
    model = Feedback

    def get_context_data(self, **kwargs):
        self.picnicid = self.kwargs['picnicid']
        context = super(CritiqueDelete, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['artworkid']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['art'] = Artwork.objects.get(id=self.kwargs['artworkid'])
        context['picnicID'] = self.kwargs['picnicid']
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Critique successfully deleted.")
        return reverse_lazy('artwork-detail', kwargs={'picnicid': self.kwargs['picnicid'],'pk':self.kwargs['artworkid']})
    
    def form_valid(self, form):
        return super().form_valid(form)

class ArtworkUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Artwork
    # success_url='/my-picnics/'
    template_name = 'mypicnics/artwork_critique_update.html'
    fields = ['title', 'description', 'feedback']

    def get_context_data(self, **kwargs):
        context = super(ArtworkUpdateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['pk']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        print(context['object'])
        print(self.kwargs)
        context['art'] = Artwork.objects.get(id=self.kwargs['pk'])
        context['update'] = "art"
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Artwork successfully updated.")
        return reverse_lazy('artwork-detail', kwargs={'picnicid': self.kwargs['picnicid'],'pk':self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.artist = self.request.user
        # form.instance.date_uploaded = form.instance.timezone
        # form.instance.key = generateKey()
        # form.instance.background_image = form.cleaned_data['background_image']
        return super().form_valid(form)

    def test_func(self):
        artwork = self.get_object()
        if self.request.user == artwork.artist:
            return True
        return False

class CritiqueUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Feedback
    # success_url='/my-picnics/'
    template_name = 'mypicnics/artwork_critique_update.html'
    fields = ['bread1', 'middle', 'bread2']

    def get_context_data(self, **kwargs):
        context = super(CritiqueUpdateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['pk']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['art'] = Artwork.objects.get(id=self.kwargs['artworkid'])
        context['update'] = "critique"
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Artwork successfully updated.")
        return reverse_lazy('artwork-detail', kwargs={'picnicid': self.kwargs['picnicid'],'pk':self.kwargs['artworkid']})

    def form_valid(self, form):
        form.instance.host = self.request.user
        # form.instance.key = generateKey()
        # form.instance.background_image = form.cleaned_data['background_image']
        return super().form_valid(form)

    def test_func(self):
        critique = self.get_object()
        if self.request.user == critique.critiquer:
            return True
        return False

@login_required
def notifications(request):
    currUser = PicnicUser.objects.get(user=request.user)
    currUser.hasNotifications = False
    currUser.save()
    context = {
        'small': True,
        'title':'Notifications',
        'pUser':currUser
    }
    if request.method == 'POST':
        for notification in currUser.notifs.all():
            notification.read = True
            notification.save()
            # print("read")
        return HttpResponse(json.dumps({'message': "hi"}))
    else:
        return render(request, 'mypicnics/notifications.html', context)

class NotifCreateView(LoginRequiredMixin, CreateView):
    model = Notification
    fields = ['extra']
    success_url='/picnic/'
    template_name="mypicnics/givethanks.html"

    def get_context_data(self, **kwargs):
        self.success_url += str(self.kwargs['picnicid']) + '/artwork/' + str(self.kwargs['artworkid'])
        context = super(NotifCreateView, self).get_context_data(**kwargs)
        context['key'] = self.kwargs['artworkid']
        context['object'] = Picnic.objects.get(id=self.kwargs['picnicid'])
        context['art'] = Artwork.objects.get(id=self.kwargs['artworkid'])
        context['picnicID'] = self.kwargs['picnicid']
        context['pUser'] = PicnicUser.objects.get(user=self.request.user)
        return context

    def form_valid(self, form):
        artwork = Artwork.objects.get(pk=self.kwargs['artworkid'])
        form.instance.message = self.request.user.username + " thanks you for your critique on \"" + artwork.title + ".\""
        form.instance.picnicid = self.kwargs['picnicid']
        form.instance.artworkid = self.kwargs['artworkid']
        form.save()
        critique = Feedback.objects.get(pk=self.kwargs['pk'])
        critique.thanks_given = True
        critique.save()
        print(artwork.artist.id)
        critiquer = PicnicUser.objects.get(user=critique.critiquer)
        critiquer.notifs.add(form.instance.id)
        critiquer.hasNotifications = True
        critiquer.save()
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        messages.success(self.request, "Your message has been sent.")
        return reverse_lazy('artwork-detail', kwargs={'picnicid': self.kwargs['picnicid'],'pk':self.kwargs['artworkid']})

def error_404(request, exception):
        context = {
            'small': True,
            'title':'Error 404',
        }
        return render(request,'mypicnics/error.html', context, status=404)

def error_500(request):
        context = {
            'small': True,
            'title':'Error 500',
        }
        return render(request,'mypicnics/error.html', context, status=500)

def error_403(request, exception):
        context = {
            'small': True,
            'title':'Error 403',
        }
        return render(request,'mypicnics/error.html', context, status=403)

def error_400(request,  exception):
        context = {
            'small': True,
            'title':'Error 400',
        }
        return render(request,'mypicnics/error.html', context, status=400)