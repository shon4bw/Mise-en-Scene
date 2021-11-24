from django.http import response
from django.http.response import JsonResponse
import requests, random
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_safe, require_POST
from django.contrib.auth.decorators import login_required
from .models import Movie, Genre
from django.core.paginator import Paginator
from django.core import serializers
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Q


# Create your views here.
# 데이터 패치(가져오기)
def fetch_movies(request):

    API_KEY = 'be07aab38070bed23b07aa9d9da3e0e2'
    TMDB_URL = 'https://api.themoviedb.org/3/'

    genres = requests.get(TMDB_URL + 'genre/movie/list' + f'?api_key={API_KEY}' + '&language=ko-kr').json().get('genres')
    for genre in genres:
        context = {
            'genre_id': genre['id'],
            'name': genre['name']
        }
        genre, created = Genre.objects.get_or_create(**context)

    for page in range(1, 6):
        
        url = f'{TMDB_URL}movie/top_rated?api_key={API_KEY}&language=ko-KR&page={page}&region=KR'
        # url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={API_KEY}&language=ko-KR&page={page}&region=KR'
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
            
            new_movie = Movie.objects.create(**context)
            
            for genre_id in movie['genre_ids']:
                genre = Genre.objects.get(genre_id=genre_id)
                new_movie.genres.add(genre)
            
            # genre, created = Genre.objects.get_or_create(name='genre_id')
            # genre.value = request.POST.get('genre_id')
            # genre.save()
            # movie.genres.add(genre)

@require_safe
def index(request):
    # movies = Movie.objects.all() -<- 여기서 할 건 이것뿐! TBDM API 주기적으로 가져오기 다른 함수에서!
    # best -> 매일 새벽 3시에 자동으로 불러오기.....
    

    # 데이터 셋 불러오기 (db 초기화시에만 주석 풀 것)
    #fetch_movies(request)


    movies = Movie.objects.all()
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
    
    user_like_movies = user.like_movies.all()
    # 리뷰목록을 하나씩 돌면서
    # 각 무비의 장르 번호만 빼올 것

    # 영화 타이틀 가지고 오기
    movie_titles= []
    for like_movie in user_like_movies :
        movie_titles.append(like_movie.movie_title) # community model

    # 전체 영화 정보를 돌면서
    # 좋아하는 영화 타이틀의 장르 번호를 가져온다
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
    
    return render(request, 'movies/mybox.html', context)


@login_required
@require_safe
def mybox(request):
    user = request.user
    
    user_like_movies = user.like_movies.all()
    # 리뷰목록을 하나씩 돌면서
    # 각 무비의 장르 번호만 빼올 것

    # 영화 타이틀 가지고 오기
    movie_titles= []
    for like_movie in user_like_movies :
        movie_titles.append(like_movie.title) # community model

    # 전체 영화 정보를 돌면서
    # 좋아하는 영화 타이틀의 장르 번호를 가져온다
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
    
    return render(request, 'movies/mybox.html', context)

@login_required
@require_POST
def create_my_box(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if request.user.like_movies.filter(pk=movie_pk).exists():
            # 현재 사용자가 좋아하는 영화목록에 지금 추가한 영화가 있으면~
            request.user.like_movies.remove(movie)
            chosen = False 
        else:
            request.user.like_movies.add(movie)
            chosen = True 
        context = {
            'chosen' : chosen,
        }
        
        return JsonResponse(context)

# 영상 재생
@login_required
def video(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        inputvalue = movie.title+'trailer'

        url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'key': settings.YOUTUBE_API_KEY,
            'part': 'snippet',
            'type': 'video',
            'maxResults': '1',
            'q': inputvalue,
        }
        response = requests.get(url, params)
        response_dict = response.json()

        context = {
            'movie': movie,
            'response_dict': response_dict,
            'youtube_items': response_dict['items']
        }
        return render(request, 'movies/video.html', context)

def pay(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if request.method == "POST":
        URL = 'https://kapi.kakao.com/v1/payment/ready'
        headers = {
            "Authorization": "KakaoAK " + "71076382b94f90106e56635f6eba4828",   # 변경불가
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",  # 변경불가
        }
        params = {
            "cid": "TC0ONETIME",    # 테스트용 코드
            "partner_order_id": "1",     # 주문번호
            "partner_user_id": "sunwoo",    # 유저 아이디
            "item_name": "기생충",        # 구매 물품 이름
            "quantity": "1",                # 구매 물품 수량
            "total_amount": "1",        # 구매 물품 가격 - 시연하기 전 금액 늘려야 함 ㅎㅎ
            "tax_free_amount": "0",         # 구매 물품 비과세
            "approval_url": f"http://localhost:8000/movies/{movie_pk}/approval/",
            "cancel_url": "http://localhost:8000/movies/",
            "fail_url": "http://localhost:8000/movies/",
        }

        res = requests.post(URL, headers=headers, params=params)   # 우리의 tid T2967728879042320529
        request.session['tid'] = res.json()['tid']      # 결제 승인시 사용할 tid를 세션에 저장
        next_url = res.json()["next_redirect_pc_url"]   # 결제 페이지로 넘어갈 url을 저장
        return redirect(next_url)

    return render(request, 'movies/pay.html')


def approval(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + "71076382b94f90106e56635f6eba4828",  
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }
    params = {
        "cid": "TC0ONETIME",    # 테스트용 코드
        "tid": request.session['tid'],  # 결제 요청시 세션에 저장한 tid
        "partner_order_id": "1",     # 주문번호
        "partner_user_id": "sunwoo",    # 유저 아이디
        "pg_token": request.GET.get("pg_token"),     # 쿼리 스트링으로 받은 pg토큰
    }

    res = requests.post(URL, headers=headers, params=params)
    amount = res.json()['amount']['total']
    res = res.json()
    context = {
        'res': res,
        'amount': amount,
        'movie' : movie,
    }
    return render(request, 'movies/approval.html', context)

def search(request):
    keyword = request.GET['keyword']

    if keyword:
        movies = Movie.objects.filter(Q(title__icontains=keyword) | Q(release_date__icontains=keyword) | Q(overview__icontains=keyword)).distinct() #SELECT * FROM Movie WHERE 두번째 Q or 첫번째 Q
        not_found = ''
        message = ''

        if len(movies) == 0:
            genres = Genre.objects.all()
            random_genre = random.randrange(0, len(genres))
            genre_id = genres[random_genre].genre_id
            g = Genre.objects.get(genre_id=genre_id)
            movies = g.movie_genres.all()
            not_found = '에 해당하는 영화가 없어요'
            message = '👇 대신 이건 어떠신가요?'

        context = {
            'keyword': keyword,
            'movies': movies,
            'not_found': not_found,
            'message': message,
        }

        return render(request, 'movies/search.html', context)
    
    
