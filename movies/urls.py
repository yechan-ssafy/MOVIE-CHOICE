from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('api/v1/', views.movie_api_url, name="movie_api_url"),
    path('api/v1/weather/', views.weather_api_url, name="weather_api_url"),
    path('', views.index, name="index"),
    path('<int:movie_id>/', views.detail, name="detail"),
    path('<int:movie_id>/like/', views.like, name="like"),
    path('<int:movie_id>/grades/', views.grade_create, name='grade_create'),
    path('<int:movie_id>/grades/<int:grade_pk>/update/', views.grade_update, name='grade_update'),
    path('<int:movie_id>/grades/<int:grade_pk>/delete/', views.grade_delete, name='grade_delete'),
    path('<str:genre_name>', views.genre_movie_list, name='genre_movie_list'),
    path('search/', views.search_movie, name='search'),
]
