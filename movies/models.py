from django.db import models
from django.conf import settings
# Create your models here.

class Movie(models.Model):
    movieid = models.IntegerField(primary_key=True )
    title = models.TextField()
    overview = models.TextField()
    original_title = models.TextField()
    popularity = models.FloatField()
    runtime = models.IntegerField()
    release_date = models.DateField()
    credit = models.TextField()
    genres = models.TextField()
    poster = models.TextField()
    videos = models.TextField()
    keywords = models.TextField()
    score = models.FloatField(default = 0)
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='like_movies',
        blank=True
    )


class Comment(models.Model):
    content= models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE
                                )
    score = models.IntegerField()


class Genre(models.Model):
    name = models.TextField()
    
class Actor(models.Model):
    name = models.CharField(max_length=30)
    gender = models.IntegerField()
    images = models.URLField()


class MG(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    popularity = models.FloatField()
class MK(models.Model):
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    genre = models.IntegerField()