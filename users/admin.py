from django.contrib import admin
from .models import PicnicUser, Notification

# Register your models here.
admin.site.register(PicnicUser)
admin.site.register(Notification)