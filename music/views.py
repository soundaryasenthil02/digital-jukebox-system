from django.shortcuts import render
from django.db.models import Count
from .models import Song, Artist, Album, PlayHistory
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count
from .models import Song, Artist, Album, PlayHistory

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