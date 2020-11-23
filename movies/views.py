from django.shortcuts import render, get_object_or_404, redirect

from .models import Movie, Genre, MovieComment
from .forms import MovieCommentForm

import requests
from pprint import pprint
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.contrib.auth.decorators import login_required

from django.db.models import Q


# Create your views here.
@login_required
@require_GET
def index(request):
    movie_list = Movie.objects.all()
    genres = Genre.objects.all()
    context = {
        'movie_list': movie_list,
        'genres': genres,
    }

    return render(request, 'movies/index.html', context)


def movie_api_url(request):
    genre_api_url = 'https://api.themoviedb.org/3/genre/movie/list?api_key=334075ba2b018bdb3e91bc504676f9b9&language=ko-kr'
    genre_res = requests.get(genre_api_url).json()

    for i in range(len(genre_res['genres'])):
        genre = Genre()
        genre.id = genre_res['genres'][i]['id']
        genre.name = genre_res['genres'][i]['name']
        genre.save()
    
    movie_api_url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=334075ba2b018bdb3e91bc504676f9b9&language=ko-kr&page='

    naver_api_url = 'https://openapi.naver.com/v1/search/movie?'
    
    header = {
        "X-Naver-Client-id" : '848DPJEM0GA39OFuYr6a',
        "X-naver-Client-secret" : '7LalejObp3'
    }


    for i in range(1, 20):
        new_movie_api_url = movie_api_url + str(i)
        res = requests.get(new_movie_api_url).json()
        confirm = 0
        for j in range(len(res['results'])):
            movies = Movie.objects.all()
            movie = Movie()
            if not res['results'][j]['genre_ids']:
                confirm = 1
            
            new_naver_api_url = naver_api_url + f'&query={res["results"][j]["title"]}&yearfrom={str(res["results"][j]["release_date"])[0:4]}&yearto={str(res["results"][j]["release_date"])[0:4]}'
            naver_res = requests.get(new_naver_api_url, headers = header).json()
            naver_movie_items = naver_res.get('items')
            if not naver_movie_items:
                confirm = 1
            else:
                actor = ''
                director = ''
                for naver_movie in naver_movie_items:
                    if naver_movie['title'] == f'<b>{res["results"][j]["title"]}</b>':
                        actor = naver_movie['actor']
                        director = naver_movie['director']
                if (not actor) or (not director):
                    confirm = 1
            
            for k in range(len(movies)):
                if str(movies[k]) == res['results'][j]['title']:
                    confirm = 1            

            if confirm == 0:
                movie.title = res['results'][j]['title']
                movie.release_date = res['results'][j]['release_date']
                movie.popularity = res['results'][j]['popularity']
                movie.vote_count = res['results'][j]['vote_count']
                movie.vote_average = res['results'][j]['vote_average']
                movie.overview = res['results'][j]['overview']
                movie.poster_path = 'https://image.tmdb.org/t/p/w500/' + res['results'][j]['poster_path']
                movie.actor = actor
                movie.director = director
                movie.save()
                for genre_id in res['results'][j]['genre_ids']:
                    movie.genres.add(get_object_or_404(Genre, id=genre_id))
                movie.save()

    return redirect('movies:index')


@login_required
@require_GET
def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comments =  movie.moviecomment_set.all()
    comment_form = MovieCommentForm()
    context = {
        'movie': movie,
        'comments': comments,
        'commnet_form': comment_form,
    }
    print(movie)
    return render(request, 'movies/detail.html', context)


@require_POST
def like(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        user = request.user

        if movie.like_users.filter(pk=user.pk).exists():
            movie.like_users.remove(user)
            is_like = False
        else:
            movie.like_users.add(user)
            is_like = True
        data = {
            'is_like' : is_like,
            'like_count': movie.like_users.count()
        }
        return JsonResponse(data)
    return redirect('accounts:login')


@require_POST
def movie_comment_create(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    comment_form = MovieCommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
        return redirect('movies:detail', movie.id)
    context = {
        'comment_form': comment_form,
        'movie': movie,
        'comments': movie.moviecomment_set.all(),
    }
    return render(request, 'movies/detail.html', context)


@require_POST
def movie_comments_delete(request, movie_id, comment_pk):
    if request.user.is_authenticated:
        comment = get_object_or_404(MovieComment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:detail', movie_id)


@login_required
@require_GET
def genre_movie_list(request, genre_name):
    genre = get_object_or_404(Genre, name=genre_name)
    movie_list = genre.genre_movie.order_by('-vote_average')[:10]
    context = {
        'genre': genre,
        'movie_list': movie_list,
    }
    return render(request, 'movies/genre_movie_list.html', context)


@login_required
@require_GET
def search_movie(request):
    movie_list = Movie.objects.all()
    
    search_keyword = request.GET.get('q', '')
    search_type = request.GET.get('type', '')

    search_movie_list = []
    if search_keyword :
        if len(search_keyword) >= 2 :
            if search_type == 'all':
                search_movie_list = movie_list.filter(Q (title__icontains=search_keyword) | Q (actor__icontains=search_keyword) | Q (overview__icontains=search_keyword))
            elif search_type == 'title':
                search_movie_list = movie_list.filter(title__icontains=search_keyword)
            elif search_type == 'actor':
                search_movie_list = movie_list.filter(actor__icontains=search_keyword)    
            elif search_type == 'director':
                search_movie_list = movie_list.filter(director__icontains=search_keyword)    
            elif search_type == 'overview':
                search_movie_list = movie_list.filter(overview__icontains=search_keyword)
                
    context = {
        'search_movie_list': search_movie_list,
    }
    return render(request, 'movies/search_movie_list.html', context)