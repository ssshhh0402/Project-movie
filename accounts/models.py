from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from movies.models import Genre
# Create your models here.


class User(AbstractUser):
    preference = models.ManyToManyField(
        Genre,
        related_name='preferences',
        blank=True
    )
