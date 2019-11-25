from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='home'),
    # path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('genre/', views.genre, name='genre'),
]