from django.db import models
from django.conf import settings
from embed_video.fields import EmbedVideoField

class Genre(models.Model):
    name = models.CharField(max_length=50)
    genre_id = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='movie_genres')
    video = EmbedVideoField(null = True)

    def __str__(self):
        return self.title

