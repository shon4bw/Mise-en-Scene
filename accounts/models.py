from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    image = models.ImageField(upload_to="", blank=True)
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

