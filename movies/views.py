from django.shortcuts import render,redirect,get_object_or_404
from . models import Movie
import datetime
import requests
from .models import Movie
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
import datetime

# Create your views here.

def index(request):
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform': loginform
    }
    return render(request, 'movies/index.html', context)

def index(request):            
    preferences = request.user.preference
    movie_list = [getNow()]
    for idx in preferences:             
        movie = Movie.objects.filter(genre = idx).order_by('-popularity')
        movie_list.append(movie[:10])
    context = {
        'movie_list' : movie_list
    }
    return render(request, 'movies/index', context)

def getNow():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')
    movie_list = []
    api_key = '407e887e6e33a30edd477d217f18d883'
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={yesterday}&multiMovieYn=N&repNationCd=K'
    response = requests.get(url).json().get('boxOfficeResult').get('dailyBoxOfficeList')
    for movie in response:
        movie_list.append(movie.get('movieNm'))
    return movie_list


