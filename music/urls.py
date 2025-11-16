from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_list, name='song_list'),
    path('top-songs/', views.top_songs, name='top_songs'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]