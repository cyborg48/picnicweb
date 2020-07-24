from django.db.models.signals import post_save
from django.dispatch import receiver
from mypicnics.models import Picnic

@receiver(post_save, sender=Picnic)
def add_picnic(sender, instance, created, **kwargs):
    if created:
        instance.host.picnicuser.picnics.add(instance.id)
        instance.members.add(instance.host)