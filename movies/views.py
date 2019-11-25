from django.shortcuts import render,redirect,get_object_or_404
from .models import Movie
from accounts.forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

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
    preferences = request.user.preference
    movie_list = []
    for idx in preferences:             #유저 preference 중 popularity 높은 애들 추가 다만 여기서 그 뭐냐 본 아이들은 뺀 작업 고려해 봐야 할 듯
                                        # 만약 넣는다고 하면, objects 받아온거 앞에서부터 하나씩 확인해야할듯
        movie = Movie.objects.filter(genre = idx).order_by('-popularity')
        movie_list.append(movie[:10])
                                            #movie_list에 지금 핫한 탑 10 넣는것도 고려
    context = {
        'movie_list' : movie_list
    }
    return render(request, 'movies/index', context)
    