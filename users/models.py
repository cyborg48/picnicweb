from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Notification(models.Model):
    message = models.TextField()
    extra = models.TextField(verbose_name="Leave a note", blank=True, help_text="Send a message to your critiquer, if you'd like! What about their feedback did you find helpful?")
    picnicid = models.IntegerField(default=0, blank=True)
    artworkid = models.IntegerField(default=0, blank=True)
    time = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

class PicnicUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    picnics = models.ManyToManyField('mypicnics.Picnic', blank=True)
    notifs = models.ManyToManyField(Notification, blank=True)
    hasNotifications = models.BooleanField(default=False, blank=True)