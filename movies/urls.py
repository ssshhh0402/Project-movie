from django.contrib import admin
from django.urls import path,include
from . import views
app_name= 'movies'
urlpatterns=[
    path('', views.index, name='index'),
    path('<int : movie_pk>/', views.detail, name='detail')
]