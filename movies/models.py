from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=50)


# class Actor(models.Model):
#     name = models.CharField(max_length=150)


# class Director(models.Model):
#     name = models.CharField(max_length=100)


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    genres = models.ManyToManyField(Genre, related_name='genre_movie')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    actor = models.CharField(max_length=150)
    director = models.CharField(max_length=100)
    # actor = models.ManyToManyField(Actor, related_name='actor_movie')
    # director = models.ManyToManyField(Director, related_name='director_movie')

    def __str__(self):
        return self.title


class MovieComment(models.Model):
    content = models.CharField(max_length=200)
    rank = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)