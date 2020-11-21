from django.shortcuts import render, get_object_or_404, redirect

from .models import Movie, Genre

import requests
from pprint import pprint

# Create your views here.
def index(request):
    movie_list = Movie.objects.all()
    context = {
        'movie_list': movie_list,
    }

    return render(request, 'movies/index.html', context)


def movie_api_url(request):
    genre_api_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=334075ba2b018bdb3e91bc504676f9b9&language=ko-kr'
    genre_res = requests.get(genre_api_url).json()
    print(genre_res)

    for i in range(len(genre_res['genres'])):
        genre = Genre()
        genre.id = genre_res['genres'][i]['id']
        genre.name = genre_res['genres'][i]['name']
        genre.save()

    
    movie_api_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=334075ba2b018bdb3e91bc504676f9b9&language=ko-kr&page='

    for i in range(1, 11):
        new_movie_api_url = movie_api_url + str(i)
        res = requests.get(new_movie_api_url).json()
        # pprint(res)

        for j in range(len(res['results'])):
            movie = Movie()
            for _ in res['results'][j]:
                movie.title = res['results'][j]['title']
                movie.release_date = res['results'][j]['release_date']
                movie.popularity = res['results'][j]['popularity']
                movie.vote_count = res['results'][j]['vote_count']
                movie.vote_average = res['results'][j]['vote_average']
                movie.overview = res['results'][j]['overview']
                movie.poster_path = 'https://image.tmdb.org/t/p/w500/' + res['results'][j]['poster_path']
            movie.save()

            # for k in range(len(res['results'][j]['genre_ids'])):
            #     genre = get_object_or_404(Genre, id=res['results'][j]['genre_ids'][k])
            #     movie_genres.movie_id = movie['id']
            #     movie_genres.genre_id = genre['id']
            #     movie_genres.save()


    return redirect('movies:index')


def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)