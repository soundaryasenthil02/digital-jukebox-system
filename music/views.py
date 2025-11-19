from django.db.models import Count
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q
from django.http import JsonResponse

from .models import Song, Artist, Album, PlayHistory, Playlist, PlaylistSong
def home(request):
    """Homepage view displaying all songs"""
    songs = Song.objects.select_related('album', 'album__artist').all()
    
    context = {
        'songs': songs,
        'total_songs': songs.count(),
    }
    return render(request, 'music/home.html', context)


def song_list(request):
    """Display all songs with search and filter"""
    songs = Song.objects.select_related('album', 'album__artist').all()
    
    # Get unique genres for filter
    genres = Song.objects.values_list('genre', flat=True).distinct()
    
    # Filter by genre if provided
    genre_filter = request.GET.get('genre')
    if genre_filter:
        songs = songs.filter(genre=genre_filter)
    
    # Search by title or artist
    search_query = request.GET.get('search')
    if search_query:
        songs = songs.filter(title__icontains=search_query) | songs.filter(album__artist__artist_name__icontains=search_query)
    
    context = {
        'songs': songs,
        'genres': genres,
        'selected_genre': genre_filter,
        'search_query': search_query,
    }
    return render(request, 'music/song_list.html', context)


def top_songs(request):
    """Display top 10 most played songs"""
    top_songs = Song.objects.annotate(
        play_count=Count('playhistory')
    ).order_by('-play_count')[:10]
    
    context = {
        'top_songs': top_songs,
    }
    return render(request, 'music/top_songs.html', context)

def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('music:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        # Validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'music/register.html')
        
        if len(password1) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return render(request, 'music/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'music/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'music/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        
        messages.success(request, f'Account created successfully! Welcome, {username}!')
        login(request, user)
        return redirect('music:home')
    
    return render(request, 'music/register.html')


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('music:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            
            # Redirect to next page if specified
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('music:home')
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'music/login.html')


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('music:home')


@login_required
def profile(request):
    """User profile view"""
    user = request.user
    
    # Get user's playlists
    user_playlists = Playlist.objects.filter(user=user).annotate(
        song_count=Count('playlistsong')
    )
    
    # Get user's play history
    recent_plays = PlayHistory.objects.filter(user=user).select_related(
        'song', 'song__album', 'song__album__artist'
    ).order_by('-played_at')[:10]
    
    # Get user's most played songs
    top_songs = Song.objects.filter(
        playhistory__user=user
    ).annotate(
        play_count=Count('playhistory')
    ).order_by('-play_count')[:5]
    
    context = {
        'user': user,
        'user_playlists': user_playlists,
        'recent_plays': recent_plays,
        'top_songs': top_songs,
        'total_plays': PlayHistory.objects.filter(user=user).count(),
    }
    
    return render(request, 'music/profile.html', context)

@login_required
def my_playlists(request):
    """Display user's playlists"""
    playlists = Playlist.objects.filter(user=request.user).annotate(
        song_count=Count('playlistsong')
    ).order_by('-created_at')
    
    context = {
        'playlists': playlists,
    }
    return render(request, 'music/my_playlists.html', context)


@login_required
def create_playlist(request):
    """Create new playlist"""
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        
        if not playlist_name or playlist_name.strip() == '':
            messages.error(request, 'Playlist name cannot be empty!')
            return render(request, 'music/create_playlist.html')
        
        # Check if user already has a playlist with this name
        if Playlist.objects.filter(user=request.user, playlist_name=playlist_name).exists():
            messages.error(request, 'You already have a playlist with this name!')
            return render(request, 'music/create_playlist.html')
        
        # Create playlist
        playlist = Playlist.objects.create(
            playlist_name=playlist_name,
            user=request.user
        )
        
        messages.success(request, f'Playlist "{playlist_name}" created successfully!')
        return redirect('music:playlist_detail', playlist_id=playlist.playlist_id)
    
    return render(request, 'music/create_playlist.html')


@login_required
def playlist_detail(request, playlist_id):
    """View playlist details and songs"""
    playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
    
    playlist_songs = PlaylistSong.objects.filter(playlist=playlist).select_related(
        'song', 'song__album', 'song__album__artist'
    )
    
    # Get all songs for adding to playlist
    all_songs = Song.objects.select_related('album', 'album__artist').all()
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        all_songs = all_songs.filter(
            Q(title__icontains=search_query) | 
            Q(album__artist__artist_name__icontains=search_query)
        )
    
    context = {
        'playlist': playlist,
        'playlist_songs': playlist_songs,
        'all_songs': all_songs,
        'search_query': search_query,
    }
    return render(request, 'music/playlist_detail.html', context)


@login_required
def edit_playlist(request, playlist_id):
    """Edit playlist name"""
    playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
    
    if request.method == 'POST':
        new_name = request.POST.get('playlist_name')
        
        if not new_name or new_name.strip() == '':
            messages.error(request, 'Playlist name cannot be empty!')
            return render(request, 'music/edit_playlist.html', {'playlist': playlist})
        
        # Check if another playlist with this name exists
        if Playlist.objects.filter(
            user=request.user, 
            playlist_name=new_name
        ).exclude(playlist_id=playlist_id).exists():
            messages.error(request, 'You already have a playlist with this name!')
            return render(request, 'music/edit_playlist.html', {'playlist': playlist})
        
        old_name = playlist.playlist_name
        playlist.playlist_name = new_name
        playlist.save()
        
        messages.success(request, f'Playlist renamed from "{old_name}" to "{new_name}"!')
        return redirect('music:playlist_detail', playlist_id=playlist.playlist_id)
    
    context = {'playlist': playlist}
    return render(request, 'music/edit_playlist.html', context)


@login_required
def delete_playlist(request, playlist_id):
    """Delete playlist"""
    playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
    
    if request.method == 'POST':
        playlist_name = playlist.playlist_name
        playlist.delete()
        messages.success(request, f'Playlist "{playlist_name}" deleted successfully!')
        return redirect('music:my_playlists')
    
    context = {'playlist': playlist}
    return render(request, 'music/delete_playlist.html', context)


@login_required
def add_to_playlist(request, playlist_id):
    """Add song to playlist"""
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
        song_id = request.POST.get('song_id')
        song = get_object_or_404(Song, song_id=song_id)
        
        # Check if song already in playlist
        if PlaylistSong.objects.filter(playlist=playlist, song=song).exists():
            messages.warning(request, f'"{song.title}" is already in this playlist!')
        else:
            PlaylistSong.objects.create(playlist=playlist, song=song)
            messages.success(request, f'Added "{song.title}" to "{playlist.playlist_name}"!')
        
        return redirect('music:playlist_detail', playlist_id=playlist.playlist_id)
    
    return redirect('music:my_playlists')


@login_required
def remove_from_playlist(request, playlist_id, song_id):
    """Remove song from playlist"""
    if request.method == 'POST':
        playlist = get_object_or_404(Playlist, playlist_id=playlist_id, user=request.user)
        song = get_object_or_404(Song, song_id=song_id)
        
        playlist_song = get_object_or_404(PlaylistSong, playlist=playlist, song=song)
        playlist_song.delete()
        
        messages.success(request, f'Removed "{song.title}" from "{playlist.playlist_name}"!')
        return redirect('music:playlist_detail', playlist_id=playlist.playlist_id)
    
    return redirect('music:my_playlists')

def analytics_dashboard(request):
    """Analytics dashboard with charts and statistics"""
    
    # Top 10 Most Played Songs
    top_songs = Song.objects.annotate(
        play_count=Count('playhistory')
    ).order_by('-play_count')[:10]
    
    # Most Popular Artists (based on total plays)
    popular_artists = Artist.objects.annotate(
        total_plays=Count('album__song__playhistory')
    ).order_by('-total_plays')[:10]
    
    # Genre Distribution
    genre_stats = Song.objects.values('genre').annotate(
        count=Count('song_id')
    ).order_by('-count')
    
    # Play History Over Time (Last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    
    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_plays = PlayHistory.objects.filter(
        played_at__gte=thirty_days_ago
    ).extra(
        select={'day': 'DATE(played_at)'}
    ).values('day').annotate(
        count=Count('play_id')
    ).order_by('day')
    
    # Overall Statistics
    total_songs = Song.objects.count()
    total_artists = Artist.objects.count()
    total_albums = Album.objects.count()
    total_plays = PlayHistory.objects.count()
    total_users = User.objects.count()
    total_playlists = Playlist.objects.count()
    
    # Most Active Users
    active_users = User.objects.annotate(
        play_count=Count('playhistory')
    ).order_by('-play_count')[:5]
    
    context = {
        'top_songs': top_songs,
        'popular_artists': popular_artists,
        'genre_stats': genre_stats,
        'daily_plays': daily_plays,
        'total_songs': total_songs,
        'total_artists': total_artists,
        'total_albums': total_albums,
        'total_plays': total_plays,
        'total_users': total_users,
        'total_playlists': total_playlists,
        'active_users': active_users,
    }
    
    return render(request, 'music/analytics.html', context)


def analytics_api(request):
    """API endpoint for chart data (JSON)"""
    chart_type = request.GET.get('type', 'top_songs')
    
    if chart_type == 'top_songs':
        top_songs = Song.objects.annotate(
            play_count=Count('playhistory')
        ).order_by('-play_count')[:10]
        
        data = {
            'labels': [song.title for song in top_songs],
            'data': [song.play_count for song in top_songs],
        }
        
    elif chart_type == 'popular_artists':
        popular_artists = Artist.objects.annotate(
            total_plays=Count('album__song__playhistory')
        ).order_by('-total_plays')[:10]
        
        data = {
            'labels': [artist.artist_name for artist in popular_artists],
            'data': [artist.total_plays for artist in popular_artists],
        }
        
    elif chart_type == 'genres':
        genre_stats = Song.objects.values('genre').annotate(
            count=Count('song_id')
        ).order_by('-count')
        
        data = {
            'labels': [item['genre'] for item in genre_stats],
            'data': [item['count'] for item in genre_stats],
        }
        
    elif chart_type == 'daily_plays':
        from django.utils import timezone
        from datetime import timedelta
        
        thirty_days_ago = timezone.now() - timedelta(days=30)
        daily_plays = PlayHistory.objects.filter(
            played_at__gte=thirty_days_ago
        ).extra(
            select={'day': 'DATE(played_at)'}
        ).values('day').annotate(
            count=Count('play_id')
        ).order_by('day')
        
        data = {
            'labels': [str(item['day']) for item in daily_plays],
            'data': [item['count'] for item in daily_plays],
        }
    else:
        data = {'labels': [], 'data': []}
    
    return JsonResponse(data)