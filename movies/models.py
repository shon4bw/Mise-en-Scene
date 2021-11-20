from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50)

class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

# class Mybox(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     movies = models.ManyToManyField(Movie, related_name='my_box_movie')
#     title = models.CharField(max_length=100)
#     poster_path = models.CharField(max_length=200)

#     def __str__(self):
#         return self.title