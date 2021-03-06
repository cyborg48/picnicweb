# Generated by Django 3.0.6 on 2020-05-27 12:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mypicnics', '0005_auto_20200527_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picnic',
            name='artworks',
            field=models.ManyToManyField(blank=True, through='mypicnics.Upload', to='mypicnics.Artwork'),
        ),
        migrations.AlterField(
            model_name='picnic',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='members', through='mypicnics.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
