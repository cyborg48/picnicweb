# Generated by Django 3.0.6 on 2020-07-05 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mypicnics', '0014_auto_20200630_1304'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='thanks_given',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
