from django.shortcuts import render, get_object_or_404, redirect

from .models import Movie

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
    # pprint(genre_res)
    
    movie_api_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=334075ba2b018bdb3e91bc504676f9b9&language=ko-kr&page='
    for i in range(1, 51):
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

    return redirect('movies:index')
