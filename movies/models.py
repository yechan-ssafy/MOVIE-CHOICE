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
    genres = models.ManyToManyField(Genre, related_name='genre_movie')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')
    actor = models.CharField(max_length=150)
    director = models.CharField(max_length=100)

    def __str__(self):
        return self.title


RATE_CHOICE = [
    (1, '1 - Trash'),
    (2, '2 - Horrible'),
    (3, '3 - Terrible'),
    (4, '4 - Bad'),
    (5, '5 - OK'),
    (6, '6 - Watchable'),
    (7, '7 - Good'),
    (8, '8 - Very Good'),
    (9, '9 - Perfect'),
    (10, '10 - Master Piece'),
]


class Grade(models.Model):
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICE)
    content = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Weather(models.Model):
    name = models.CharField(max_length=50)