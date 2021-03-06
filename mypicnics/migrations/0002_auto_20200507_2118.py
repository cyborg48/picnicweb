# Generated by Django 3.0.5 on 2020-05-07 21:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mypicnics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('artwork', models.ImageField(upload_to='artworks')),
                ('description', models.TextField()),
                ('feedback', models.TextField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='picnic',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='host', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Upload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_uploaded', models.DateField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypicnics.Artwork')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypicnics.Picnic')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=100)),
                ('is_admin', models.BooleanField(default=False)),
                ('date_joined', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypicnics.Picnic')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bread1', models.TextField()),
                ('middle', models.TextField()),
                ('bread2', models.TextField()),
                ('critiquer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Critique',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateField()),
                ('artwork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypicnics.Artwork')),
                ('critique', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mypicnics.Feedback')),
            ],
        ),
        migrations.AddField(
            model_name='artwork',
            name='critiques',
            field=models.ManyToManyField(through='mypicnics.Critique', to='mypicnics.Feedback'),
        ),
        migrations.AddField(
            model_name='picnic',
            name='artworks',
            field=models.ManyToManyField(through='mypicnics.Upload', to='mypicnics.Artwork'),
        ),
        migrations.AddField(
            model_name='picnic',
            name='members',
            field=models.ManyToManyField(related_name='members', through='mypicnics.Membership', to=settings.AUTH_USER_MODEL),
        ),
    ]
