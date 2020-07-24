from django import forms
from .models import Picnic, Artwork, Feedback
from django.forms import ModelForm

class PicnicJoinForm(ModelForm):

    class Meta:
        model = Picnic
        fields = ['key']

class ArtworkCreateForm(ModelForm):

    class Meta:
        model = Artwork
        fields = ['title', 'artwork', 'description', 'feedback']


class CritiqueForm(ModelForm):

    class Meta:
        model = Feedback
        fields = ['bread1', 'middle', 'bread2']