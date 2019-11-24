from django.contrib import admin
from django.urls import path,include
from . import views
app_name = 'accounts'
urlpattenrs=[
    path('', views.index, name='home')
    path('signup/', views.signup, name='signup')
    path('profile/', views.profile, name='profile')
]