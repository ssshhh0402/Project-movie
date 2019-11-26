from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie, Genre
from accounts.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from IPython import embed
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
    #movie_list = [getNow()]
    movie_list = []
    for idx in user.preference.all():   
        genre_movie = {}
        genre_movie['genre'] = Genre.objects.get(id=idx.id).name
        movie = Movie.objects.filter(genres__contains= idx.id).order_by('-popularity')
        genre_movie['genre_movie_list'] = movie[:10]
        movie_list.append(genre_movie)

    # for idx in range(3):
    #     movie = Movie.objects.filter(genres__contains=preference_list[idx].id).order_by('-popularity')
    #     movie_list.append(movie[:10])
    context = {
        # 'genre_list' : preference_list,
        'movie_list' : movie_list
    }
    return render(request, 'movies/index.html', context)

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, id=movie_pk)
    genre_list = []
    movie_genre_list = eval(movie.genres)
    for genre in movie_genre_list:
        genre_item = Genre.objects.get(id=genre)
        genre_list.append(genre_item.name)
    movie.genres = genre_list
    movie.credit = eval(movie.credit)
    context = {
        'movie' : movie
    }
    return render(request,'movies/detail.html', context)
    
def getNow():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')
    movie_list = []
    api_key = '407e887e6e33a30edd477d217f18d883'
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={yesterday}&multiMovieYn=N&repNationCd=K'
    response = requests.get(url).json().get('boxOfficeResult').get('dailyBoxOfficeList')
    for movie in response:
        try:
            item = Movie.objects.get(title=movie.get('movieNm'))
            movie_list.append(item)
        except:
            movie_title = movie.get('movieNm')
            find_url = f'https://api.themoviedb.org/3/search/movie?api_key={key}&language=ko-KR&query={movie_title}&page=1&include_adult=true'
            response_2 = requests.get(find_url).json().get('result')[0]
            movie_id = response_2.get('id')
            detail_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=ko-KR&append_to_response=videos%2Ccredits'
            response_detail = requests.get('detail_url').json()
            genre_list = []
            video_list = []
            for genre in response_detail.get('genres'):
                genre_list.append(genre.get('id'))
            if response_detail.get('videos').get('results'):
                for movie in response_detail.get('videos').get('result'):
                    video_list.append(movie.get('key'))
            else:
                detail_url2 = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US&append_to_response=videos%2Ccredits'
                response_detail_en = requests.get(detail_url2).json()
                if response_detail_en.get('videos').get('result'):
                    for movie in response_detail_en.get('videos').get('result'):
                        video_list.append(movie.get('key'))
            movie = Movie().objects.create(movieid=response_detail.get('id'),title=response_detail.get('title'), overview=response_detail.get('overview'), genres=genre_list, poster=response_detail.get('poster_path'), original_title=response_detail.get('original_title'), popularity= response_detail.get('popularity'), runtime= response_detail.get('runtime'), release_date=response_detail.get('release_date'), videos = video_list, credit = response_detail.get('credits').get('cast'))
            movie_list.append(movie)
    

    return movie_list


