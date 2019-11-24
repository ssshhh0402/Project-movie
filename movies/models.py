from django.db import models
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    movieId = models.IntegerField()
    title = models.TextField()
    original_title = models.TextField()
    popularity = models.FloatField()
    runtime = models.IntegerField()
    release_date = models.DateField()
    credit = models.TextField()
    genres = models.TextField()

class Genre(models.Model):
    genre_num = models.IntegerField()
    genre_name = models.TextField()
    