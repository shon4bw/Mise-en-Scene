from django.http.response import JsonResponse
import requests, random
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe
from .models import Movie, Genre
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings


# Create your views here.
@require_safe
def index(request):
    # movies = Movie.objects.all()
    # paginator = Paginator(movies, 10)

    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # # /movies/?page=2 ajax 요청 => json
    # if request.headers.get('x-requested-with') == 'XMLHttpRequest':
    #     data = serializers.serialize('json', page_obj)
    #     return HttpResponse(data, content_type='application/json')
    # # /movies/ 첫번째 페이지 요청 => html
    # else:
    #     context = {
    #         'movies': page_obj,
    #     }

    #     return render(request, 'movies/index.html', context)

    # TMDB data 뿌려주기
    for page in range(1, 6):
        API_KEY = 'be07aab38070bed23b07aa9d9da3e0e2'
        url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=ko-KR&page={page}&region=KR'
        movie_dict = requests.get(url).json()
        movies = movie_dict.get('results')
        for movie in movies:
            context = {
                # "tmdb_id": movie.get('id'),
                "title" : movie.get('title'),
                "release_date": movie.get('release_date'),
                "popularity": movie.get('popularity'),
                "vote_count": movie.get('vote_count'),
                "vote_average": movie.get('vote_average'),
                "overview": movie.get('overview'),
                "poster_path": movie.get('poster_path'),
            }
            movie = Movie.objects.create(**context)
            genre, created = Genre.objects.get_or_create(name='genre_id')
            genre.value = request.POST.get('genre_id')
            genre.save()
            movie.genres.add(genre)
        movies = Movie.objects.all()
        for movie in movies:
            movie.genres.all()
    context = {
        'movies' : movies
    }
    return render(request, 'movies/index.html', context)


@require_safe
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {
        'movie' : movie,
    }
    return render(request, 'movies/detail.html', context)


@require_safe
def recommended(request):
    user = request.user
    # 선우가 좋아하는 리뷰 목록
    user_like_reviews = user.like_reviews.all()
    # 리뷰목록을 하나씩 돌면서
    # 각 리뷰의 장르 번호만 빼올 것

    # 각 리뷰의 영화 타이틀 가지고 오기
    movie_titles= []
    for review in user_like_reviews :
        movie_titles.append(review.movie_title) # community model

    # 전체 영화 정보를 돌면서
    # 선우가 좋아하는 영화 타이틀의 장르 번호를 가져온다
    genre_nums = []
    for movie_title in movie_titles:
        genre_num_list = Movie.objects.filter(title=movie_title).values('genres')
        for genre_num in genre_num_list:
            genre_nums.append(genre_num['genres'])
            # ['기생충', '대부 2', '너의 이름은.'] [18, 35, 53, 18, 80, 16, 18, 10749]

    # 각 장르 번호를 세줘서 가장 많이 등장하는 장르 뽑기
    genre_nums_set = list(set(genre_nums))
    max_genre_num = genre_nums_set[0]
    max_genre_num_cnt = genre_nums_set.count(max_genre_num)
    for genre_num in genre_nums_set: 
        if genre_nums.count(genre_num) > max_genre_num_cnt :
            max_genre_num = genre_num
            max_genre_num_cnt = genre_nums.count(genre_num)
            # 18 뽑음
    
    recommended_movies = []
    for movie in Movie.objects.all():
        if movie.genres.filter(pk=max_genre_num).exists() :
            recommended_movies.append(movie)

    random_movies = random.sample(recommended_movies, 10)

    context = {
        'random_movies': random_movies
    }
    
    return render(request, 'movies/recommended.html', context)

@require_safe
def mybox(request):
    return render(request, 'movies/mybox.html')

def create_my_box(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.user.like_movies.filter(pk=movie_pk).exists():
            # 현재 사용자가 좋아하는 영화목록에 지금 추가한 영화가 있으면~
            request.user.like_movies.remove(movie)
        else:
            request.user.like_movies.add(movie)

        return redirect('movies:mybox')

# 영상 재생
def video(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        # context = {
        #     'movie' : movie,
        # }
        # return render(request, 'movies/video.html', context)
        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'key': settings.YOUTUBE_API_KEY,
            'part': 'snippet',
            'type': 'video',
            'maxResults': '3',
            'q': '쇼생크탈출',
        }
        response = requests.get(url, params)
        response_dict = response.json()

        context = {
            'movie': movie,
            'youtube_items': response_dict['items']
        }
        return render(request, 'movies/video.html', context)