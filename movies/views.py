from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Genre
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from IPython import embed
from .forms import CommentForm
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import datetime
import requests
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        return redirect('movies:index')
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform': loginform
    }
    return render(request, 'movies/home.html', context)

def index(request):
    User = get_user_model()
    user = get_object_or_404(User, username=request.user)
    if user.preference.all():
        now_list = getNow()
        movie_list = []
        for idx in user.preference.all():   
            genre_movie = {}
            genre_movie['genre'] = Genre.objects.get(id=idx.id).name
            movie = Movie.objects.filter(genres__contains= idx.id).order_by('-popularity')
            genre_movie['genre_movie_list'] = movie[:10]
            movie_list.append(genre_movie)
        context = {
            'movie_list' : movie_list,
            'now' : now_list
        }
        return render(request, 'movies/index.html', context)
    else:
        return redirect('accounts:genre')

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, movieid=movie_pk)
    genre_list = []
    movie_genre_list = eval(movie.genres)
    for genre in movie_genre_list:
        genre_item = Genre.objects.get(id=genre)
        genre_list.append(genre_item.name)
    movie.genres = genre_list
    video_list = ''
    if eval(movie.videos):
        video_list = (eval(movie.videos)[0])
    movie.videos = video_list
    movie.credit = eval(movie.credit)
    re_movie = get_re(movie_pk)
    comments = movie.comment_set.all()
    comment_form = CommentForm()
    context = {
        'movie': movie,
        're_movie' : re_movie,
        'comments' : comments,
        'comment_form' : comment_form
    }
    print(movie.like_users)
    return render(request,'movies/detail.html', context)
    
def getNow():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')
    movie_list = []
    api_key = '407e887e6e33a30edd477d217f18d883'
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={yesterday}&multiMovieYn=N'
    a = requests.get(url).json()
    response = requests.get(url).json().get('boxOfficeResult').get('dailyBoxOfficeList')
    api_key = '69855813cd52f7cdbc7e336c8afaac95'
    for movie in response:
        try:
            item = Movie.objects.get(title=movie.get('movieNm'))
            movie_list.append(item)
        except:
            movie_title = movie.get('movieNm')
            find_url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&language=ko-KR&query={movie_title}&page=1&include_adult=true'
            response_2 = requests.get(find_url).json().get('results')
            if response_2:
                movie_id = response_2[0].get('id')
            else:
                continue
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR&append_to_response=videos%2Ccredits'
            response_detail = requests.get(detail_url).json()
            genre_list = []
            video_list = []
            for genre in response_detail.get('genres'):
                genre_list.append(genre.get('id'))
            a = response_detail.get('videos').get('results')
            if a:
                for movie in a:
                    video_list.append(movie.get('key'))
            else:
                detail_url2 = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US&append_to_response=videos%2Ccredits'
                response_detail_en = requests.get(detail_url2).json()
                if response_detail_en.get('videos').get('result'):
                    for movie in response_detail_en.get('videos').get('result'):
                        video_list.append(movie.get('key'))
            movie = Movie.objects.create(movieid=response_detail.get('id'),title=response_detail.get('title'), overview=response_detail.get('overview'), genres=genre_list, poster=response_detail.get('poster_path'), original_title=response_detail.get('original_title'), popularity= response_detail.get('popularity'), runtime= response_detail.get('runtime'), release_date=response_detail.get('release_date'), videos = video_list, credit = response_detail.get('credits').get('cast'))
            movie_list.append(movie)
    return movie_list

def get_re(a):
    api_key = '69855813cd52f7cdbc7e336c8afaac95'
    url = f'https://api.themoviedb.org/3/movie/{a}/recommendations?api_key={api_key}&language=ko-KR&page=1'
    response= requests.get(url).json().get('results')
    movie_list = []
    
    recommendation_list = []
    if not response:                                # 추천 영화 없으면
        return recommendation_list
    for i in range(10):
        movie_list.append(response[i].get('id'))
    for movie in movie_list:
        genre_list = []
        video_list = []
        try:
            item = Movie.objects.get(movieid=movie)
            recommendation_list.append(item)
        except:
            url = f'https://api.themoviedb.org/3/movie/{movie}?api_key={api_key}&language=ko-KR&append_to_response=videos%2Ccredits'
            #response = requests.get(url).json().get('result')
            response = requests.get(url).json()
            for genre in response.get('genres'):
                genre_list.append(genre.get('id'))
            videos = response.get('videos').get('results')
            if videos:
                for video in videos:
                    video_list.append(video.get('key'))
            else:
                url_en = f'https://api.themoviedb.org/3/movie/{movie}?api_key={api_key}&language=en-US&append_to_response=videos%2Ccredits'
                response_en = requests.get(url_en).json().get('videos').get('results')
                if response_en:
                    for video in response_en:
                        video_list.append(video.get('key'))
            movie_item = Movie.objects.create(movieid=movie, title=response.get('title'), overview=response.get('overview'), genres=genre_list, poster=response.get('poster_path'), original_title=response.get('original_title'), popularity=response.get('popularity'), runtime=response.get('runtime'), release_date = response.get('release_date'),videos=video_list,credit=response.get('credits').get('cast'))
            recommendation_list.append(movie_item)
    return recommendation_list

########################################댓글#########################
@require_POST
def comment_create(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, movieid=movie_pk)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.movie = movie
            comment.user = request.user
            comment.save()
            embed()
            return redirect('movies:detail', movie_pk)
        # 타당하지 않을 경우 Alert 창 띄우면 될것같은데...
    else:
        return HttpResponse('Unauthorized', status=401)


@require_POST   
def comment_delete(request, movie_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('movies:detail', movie_pk)
########################################좋아요############################

def like(request, movie_pk):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, movieid=movie_pk)
        if request.user in movie.like_users.all():
            movie.like_users.remove(request.user)
        else:
            movie.like_users.add(request.user)
        return redirect('movies:detail', movie_pk)
    else:
        return redirect('accounts:login')
###########################################################################

