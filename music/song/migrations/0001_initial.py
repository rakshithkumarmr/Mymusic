# Generated by Django 2.2.13 on 2020-09-08 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=1000)),
                ('singer', models.CharField(max_length=1000)),
                ('tags', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='song_images/')),
                ('song', models.FileField(upload_to='song')),
                ('movie_name', models.CharField(max_length=100)),
            ],
        ),
    ]
