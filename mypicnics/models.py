from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from django.contrib import admin
from django import forms

# Create your models here.

class Feedback(models.Model):
    bread1 = models.TextField(verbose_name="Layer 1 - Bread", help_text="Open with a compliment. What first strikes you about this piece and why?")
    middle = models.TextField(verbose_name="Layer 2 - Filling", help_text="Here is where you will put the 'meat' of your critique. What could be improved or refined? Keep in mind the aspects that the artist specifically wanted feedback on.")
    bread2 = models.TextField(verbose_name="Layer 3 - Bread", help_text="Close off with another positive comment. What do you like about this piece overall? How does it make you feel? Do you have any questions about this piece?")
    critiquer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(default=timezone.now, blank=True)
    thanks_given = models.BooleanField(default=False, blank=True)

class Img(models.Model):
    img = models.ImageField(upload_to="artworks")

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.img.path)

        if img.height > 700 or img.width > 700:
            if img.height > img.width:
                output_size = (700, 700*(img.width / img.height))
            else:
                output_size = (700*(img.height / img.width), 700)
            # output_size = (2000, 2000)
            img.thumbnail(output_size)
            img.save(self.img.path)

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    cover = models.ForeignKey(Img, on_delete=models.CASCADE, related_name="cover", null=True, default=None)
    artwork = models.ManyToManyField(Img)
    description = models.TextField(help_text="Describe this piece, the mediums you used, the ideas behind it, etc.")
    feedback = models.TextField(help_text="What aspects of this piece would you like feedback on? (color, composition, anatomy, etc.)")
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    critiques = models.ManyToManyField(Feedback, through='Critique')
    date_uploaded = models.DateTimeField(default=timezone.now, blank=True)

    '''

    def save(self):
        super().save()
        artwork = Image.open(self.artwork.path)

        if artwork.height > 1500 or artwork.width > 1500:
            if artwork.height > artwork.width:
                output_size = (1500, 1500*(artwork.width / artwork.height))
            else:
                output_size = (1500*(artwork.height / artwork.width), 1500)
            # output_size = (2000, 2000)
            artwork.thumbnail(output_size)
            artwork.save(self.artwork.path)
    '''

class Picnic(models.Model):
    name = models.CharField(max_length=100)
    background_image = models.ImageField(default='backgrounds/default.png', upload_to='backgrounds', help_text="Upload a background image for your picnic.", blank=False, null=False)
    description = models.TextField(help_text="Enter a description of your picnic.")
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="host")
    key = models.CharField(max_length=100)
    members = models.ManyToManyField(User, through='Membership', related_name="members", blank=True)
    artworks = models.ManyToManyField(Artwork, through='Upload', blank=True)

    def __str__(self):
        return self.name

    def save(self):
        super().save()
        background_image = Image.open(self.background_image.path)

        if background_image.height > 2500 or background_image.width > 2500:
            if background_image.height > background_image.width:
                output_size = (2500, 2500*(background_image.width / background_image.height))
            else:
                output_size = (2500*(background_image.height / background_image.width), 2500)
            # output_size = (2000, 2000)
            background_image.thumbnail(output_size)
            background_image.save(self.background_image.path)

class Membership(models.Model):
    group = models.ForeignKey(Picnic, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateField(default=timezone.now)
    num_uploads = models.IntegerField(default=0)
    num_critiques = models.IntegerField(default=0)

class Upload(models.Model):
    artwork = models.OneToOneField(Artwork, on_delete=models.CASCADE)
    group = models.ForeignKey(Picnic, on_delete=models.CASCADE)

class Critique(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    critique = models.OneToOneField(Feedback, on_delete=models.CASCADE)