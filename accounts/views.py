from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
# Create your views here.

def index(request):                 #맨처음 로그인 폼 보여주는 페이지
                                    #post => 로그인 진행, get => 로그인 폼
    if request.user.is_authenticated:
        return redirect('movies:index')
    if request.method == 'POST':
        form = AuthenticationForm(request.POST, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('movies:index')
        #여기다가 아이디, 비번 틀렸을 때 하는 행동 넣어야 할듯 아마도..?
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

    def signup(request):            #'GET'이면 폼보여주고
                                        #'POST'면 입력받은 정보 저장하면서 로그인 진행
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                return redirect('movies:index')
        else:
            form = CustomUserCreationForm()
        context = {
            'form' : form
        }
        return render(request, 'moveis/form.html', context)
    
    def logout(request):
        auth_logout(request)
        return rediret('accounts:home')
    
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