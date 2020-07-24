from django.contrib import admin
from .models import Picnic, Artwork, Feedback, Membership

# Register your models here.

class PicnicMember(admin.TabularInline):
    model = Membership

class PicnicMembership(admin.ModelAdmin):
    inlines = (PicnicMember,)

admin.site.register(Picnic, PicnicMembership)
admin.site.register(Artwork)
admin.site.register(Feedback)