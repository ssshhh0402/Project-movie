from django.contrib import admin
from django.urls import path,include
from . import views
app_name= 'movies'
urlpatterns=[
    path('', views.index, name='index'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/comment/', views.comment_create, name='c_comment'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('<int:movie_pk>/comment/<int:comment_pk>/', views.comment_delete,name='c_delete'),
]