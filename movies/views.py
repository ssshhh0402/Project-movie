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
    signupform = CustomUserCreationForm()
    loginform = AuthenticationForm()
    context = {
        'signupform': signupform,
        'loginform': loginform
    }
    return render(request, 'movies/home.html', context)

def index(request):
    preferences = request.user.preference
    User = get_user_model()
    user = get_object_or_404(User, username=request.user)
    movie_list = [getNow()]            
    for idx in user.preference.all():   
        movie = Movie.objects.filter(genres__contains= idx.id).order_by('-popularity')
        movie_list.append(movie[:10])
    
    context = {
        'movie_list' : movie_list
    }
    return render(request, 'movies/index.html', context)

def getNow():
    yesterday = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday.strftime('%Y%m%d')
    movie_list = []
    api_key = '407e887e6e33a30edd477d217f18d883'
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={api_key}&targetDt={yesterday}&multiMovieYn=N&repNationCd=K'
    response = requests.get(url).json().get('boxOfficeResult').get('dailyBoxOfficeList')
    for movie in response:
        item = Movie.objects.get(title=movie.get('movieNm'))
        movie_list.append(item)
    return movie_list


