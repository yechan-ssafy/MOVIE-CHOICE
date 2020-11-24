from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('api/v1/', views.movie_api_url, name="movie_api_url"),
    path('api/v1/weather/', views.weather_api_url, name="weather_api_url"),
    path('', views.index, name="index"),
    path('<int:movie_id>/', views.detail, name="detail"),
    path('<int:movie_id>/like/', views.like, name="like"),
    path('<int:movie_id>/comments/', views.movie_comment_create, name='movie_comment_create'),
    path('<int:movie_id>/comments/<int:comment_pk>/update/', views.movie_comments_update, name='movie_comments_update'),
    path('<int:movie_id>/comments/<int:comment_pk>/delete/', views.movie_comments_delete, name='movie_comments_delete'),
    path('<str:genre_name>', views.genre_movie_list, name='genre_movie_list'),
    path('search/', views.search_movie, name='search'),
]
