from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=100)
    country = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'artists'
    
    def __str__(self):
        return self.artist_name


class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    album_name = models.CharField(max_length=100)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    release_year = models.IntegerField(null=True, blank=True)
    
    class Meta:
        db_table = 'albums'
    
    def __str__(self):
        return self.album_name


class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    duration = models.IntegerField(help_text="Duration in seconds")
    genre = models.CharField(max_length=50, blank=True)
    file_link = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'songs'
    
    def __str__(self):
        return self.title


class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'playlists'
    
    def __str__(self):
        return self.playlist_name


class PlaylistSong(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'playlist_songs'
        unique_together = ('playlist', 'song')
    
    def __str__(self):
        return f"{self.playlist.playlist_name} - {self.song.title}"


class PlayHistory(models.Model):
    play_id = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'play_history'
    
    def __str__(self):
        return f"{self.user.username} played {self.song.title}"
    

class Queue(models.Model):
    queue_id = models.AutoField(primary_key=True)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    is_playing = models.BooleanField(default=False)
    played = models.BooleanField(default=False)
    position = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'queue'
        ordering = ['position', 'added_at']
    
    def __str__(self):
        status = "Playing" if self.is_playing else ("Played" if self.played else "Queued")
        return f"{self.song.title} - {status}"