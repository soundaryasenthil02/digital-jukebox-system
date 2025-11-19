from django.contrib import admin
from .models import Artist, Album, Song, Playlist, PlaylistSong, PlayHistory, Queue

# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('artist_id', 'artist_name', 'country')
    search_fields = ('artist_name', 'country')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('album_id', 'album_name', 'artist', 'release_year')
    list_filter = ('release_year', 'artist')
    search_fields = ('album_name', 'artist__artist_name')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('song_id', 'title', 'album', 'genre', 'duration')
    list_filter = ('genre', 'album')
    search_fields = ('title', 'genre')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('playlist_id', 'playlist_name', 'user', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('playlist_name', 'user__username')


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ('playlist', 'song')
    list_filter = ('playlist',)


@admin.register(PlayHistory)
class PlayHistoryAdmin(admin.ModelAdmin):
    list_display = ('play_id', 'song', 'user', 'played_at')
    list_filter = ('played_at', 'user')
    search_fields = ('song__title', 'user__username')

@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = ('queue_id', 'song', 'user', 'position', 'is_playing', 'played', 'added_at')
    list_filter = ('is_playing', 'played', 'user')
    search_fields = ('song__title', 'user__username')
    ordering = ('position', 'added_at')