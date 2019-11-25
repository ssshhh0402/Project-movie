from django.shortcuts import render,redirect,get_object_or_404
<<<<<<< HEAD
from . models import Movie
import datetime
import requests
=======
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

# 영화목록 
def lists(request):             # 여기서 갑자기 든 생각인데 User model 한테 watched list  혹은 Movie model한테 watched people list 주면 어떨까 싶습니다.
>>>>>>> 40be385786c2d62ba7c853298e7974b3e07ca074
# Create your views here.
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


