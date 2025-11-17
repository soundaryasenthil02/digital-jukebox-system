from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('', views.home, name='home'),
    path('songs/', views.song_list, name='song_list'),
    path('top-songs/', views.top_songs, name='top_songs'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Playlist URLs
    path('playlists/', views.my_playlists, name='my_playlists'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    path('playlists/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/edit/', views.edit_playlist, name='edit_playlist'),
    path('playlists/<int:playlist_id>/delete/', views.delete_playlist, name='delete_playlist'),
    path('playlists/<int:playlist_id>/add/', views.add_to_playlist, name='add_to_playlist'),
    path('playlists/<int:playlist_id>/remove/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),
]