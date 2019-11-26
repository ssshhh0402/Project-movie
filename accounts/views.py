from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from IPython import embed
from movies.models import Genre
# Create your views here.

def login(request):
    form = AuthenticationForm(request.POST, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        if not user.preference.all():
            return redirect('accounts:genre')
        else:
            return redirect('movies:index')
    else:
        return redirect('/')
    

def signup(request):            #'GET'이면 폼보여주고
                                        #'POST'면 입력받은 정보 저장하면서 로그인 진행
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return redirect('accounts:genre')
    else:
        # 비밀번호가 잘못됐습니다 경고문 띄우기
        return render(request, 'movies/home.html')

def genre(request):
    genres = Genre.objects.all()
    context = {
        'genres': genres
    }
    if request.method == 'POST':
        user = request.user
        genres = request.POST.getlist('genre')
        for pk in genres:
            user.preference.add(pk)
        return redirect('movies:index')
    else:
        return render(request, 'accounts/genre.html', context)

def logout(request):
    auth_logout(request)
    return redirect('/')
    
def profile(request):                    # request.user의 정보 받아오기
    User = get_user_model()
    user = get_object_or_404(User, pk=request.user.pk)
    context = {
        'user' : user
    }
    return render(request, 'accounts/profile.html', context)
        
def update(request):                       # POST 면 변경 후 바뀐 프로필 보여주기
                                                    # GET이면 유저 정보 변경 Form 보여주기
    if request.method == 'POST':                   
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)