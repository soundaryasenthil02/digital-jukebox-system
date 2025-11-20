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

    # Analytics URLs
    path('analytics/', views.analytics_dashboard, name='analytics'),
    path('api/analytics/', views.analytics_api, name='analytics_api'),

    # Jukebox Queue URLs
    path('jukebox/', views.jukebox_queue, name='jukebox_queue'),
    path('jukebox/add/', views.add_to_queue, name='add_to_queue'),
    path('jukebox/remove/<int:queue_id>/', views.remove_from_queue, name='remove_from_queue'),
    path('jukebox/play-next/', views.play_next, name='play_next'),
    path('jukebox/skip/', views.skip_song, name='skip_song'),
    path('jukebox/clear/', views.clear_queue, name='clear_queue'),
    path('songs/<int:song_id>/play/', views.play_song, name='play_song'),
]