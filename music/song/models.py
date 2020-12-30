from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    singer = models.CharField(max_length=1000)
    tags = models.CharField(max_length=100)
    image = models.ImageField(upload_to="song_images/")
    song = models.FileField(upload_to='song')
    movie_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Listenlater(models.Model):
    listen_id =  models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=100)

class History(models.Model):
    hist_id =  models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    audio_id = models.CharField(max_length=100)

class Channel(models.Model):
    channel_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    music = models.CharField(max_length=1000)