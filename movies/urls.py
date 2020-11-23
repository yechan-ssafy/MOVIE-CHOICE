from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('api/v1/', views.movie_api_url, name="movie_api_url"),
    path('', views.index, name="index"),
    path('<int:movie_id>/', views.detail, name="detail"),
    path('<int:movie_id>/like/', views.like, name="like"),
    path('<int:movie_id>/comments/', views.create_comment, name='create_comment'),
    path('<str:genre_name>', views.genre_movie_list, name='genre_movie_list'),
    path('search/', views.search_movie, name='search'),
]
