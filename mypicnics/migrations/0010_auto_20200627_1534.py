# Generated by Django 3.0.6 on 2020-06-27 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypicnics', '0009_auto_20200627_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='artwork',
            field=models.ImageField(upload_to='artworks'),
        ),
    ]
