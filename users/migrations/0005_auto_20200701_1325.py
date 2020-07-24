# Generated by Django 3.0.6 on 2020-07-01 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200630_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='link',
        ),
        migrations.AddField(
            model_name='notification',
            name='artworkid',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='notification',
            name='picnicid',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
