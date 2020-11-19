from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.index, name="index"),
    path('api/v1/', views.movie_api_url, name="movie_api_url"),
]
