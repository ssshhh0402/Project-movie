from django.db import models
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    title = models.TextField()
    original_title = models.TextField()
    popularity = models.FloatField()
    runtime = models.IntegerField()
    release_date = models.DateField()
    credit = models.TextField()
    genres = models.TextField()
    poster = models.TextField()
    videos = models.TextField()

class Genre(models.Model):
    name = models.TextField()
    
class Actor(models.Model):
    name = models.CharField(max_length=30)
    gender = models.IntegerField()
    images = models.URLField()