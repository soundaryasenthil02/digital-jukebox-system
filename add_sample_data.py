import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jukebox_project.settings')
django.setup()

from django.contrib.auth.models import User
from music.models import Artist, Album, Song, Playlist, PlaylistSong, PlayHistory
from datetime import datetime, timedelta
import random

def clear_existing_data():
    """Clear existing data to avoid duplicates"""
    print("Clearing existing data...")
    PlayHistory.objects.all().delete()
    PlaylistSong.objects.all().delete()
    Playlist.objects.all().delete()
    Song.objects.all().delete()
    Album.objects.all().delete()
    Artist.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()
    print("✓ Data cleared")

def create_users():
    """Create 15 users"""
    print("\nCreating users...")
    users = []
    
    # Create cafe owner
    owner = User.objects.create_user(
        username='cafe_owner',
        email='owner@cafejukebox.com',
        password='owner123',
        first_name='Sarah',
        last_name='Johnson'
    )
    users.append(owner)
    
    # Create regular customers
    customer_names = [
        ('john_doe', 'John', 'Doe'),
        ('emma_wilson', 'Emma', 'Wilson'),
        ('michael_brown', 'Michael', 'Brown'),
        ('sophia_davis', 'Sophia', 'Davis'),
        ('james_miller', 'James', 'Miller'),
        ('olivia_garcia', 'Olivia', 'Garcia'),
        ('william_martinez', 'William', 'Martinez'),
        ('ava_rodriguez', 'Ava', 'Rodriguez'),
        ('robert_hernandez', 'Robert', 'Hernandez'),
        ('isabella_lopez', 'Isabella', 'Lopez'),
        ('david_gonzalez', 'David', 'Gonzalez'),
        ('mia_perez', 'Mia', 'Perez'),
        ('joseph_sanchez', 'Joseph', 'Sanchez'),
        ('charlotte_ramirez', 'Charlotte', 'Ramirez'),
    ]
    
    for username, first, last in customer_names:
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='password123',
            first_name=first,
            last_name=last
        )
        users.append(user)
    
    print(f"✓ Created {len(users)} users")
    return users

def create_artists():
    """Create 20 artists"""
    print("\nCreating artists...")
    artists_data = [
        ('Taylor Swift', 'USA'),
        ('Ed Sheeran', 'UK'),
        ('Billie Eilish', 'USA'),
        ('The Weeknd', 'Canada'),
        ('Ariana Grande', 'USA'),
        ('Drake', 'Canada'),
        ('Adele', 'UK'),
        ('Post Malone', 'USA'),
        ('Dua Lipa', 'UK'),
        ('Harry Styles', 'UK'),
        ('Olivia Rodrigo', 'USA'),
        ('Bad Bunny', 'Puerto Rico'),
        ('Justin Bieber', 'Canada'),
        ('Bruno Mars', 'USA'),
        ('Doja Cat', 'USA'),
        ('Shawn Mendes', 'Canada'),
        ('Sam Smith', 'UK'),
        ('Lil Nas X', 'USA'),
        ('Coldplay', 'UK'),
        ('Imagine Dragons', 'USA'),
    ]
    
    artists = []
    for name, country in artists_data:
        artist = Artist.objects.create(artist_name=name, country=country)
        artists.append(artist)
    
    print(f"✓ Created {len(artists)} artists")
    return artists

def create_albums(artists):
    """Create 25 albums"""
    print("\nCreating albums...")
    albums_data = [
        ('Midnights', artists[0], 2022),
        ('Divide', artists[1], 2017),
        ('Happier Than Ever', artists[2], 2021),
        ('After Hours', artists[3], 2020),
        ('Thank U, Next', artists[4], 2019),
        ('Certified Lover Boy', artists[5], 2021),
        ('30', artists[6], 2021),
        ('Hollywood\'s Bleeding', artists[7], 2019),
        ('Future Nostalgia', artists[8], 2020),
        ('Harry\'s House', artists[9], 2022),
        ('SOUR', artists[10], 2021),
        ('Un Verano Sin Ti', artists[11], 2022),
        ('Justice', artists[12], 2021),
        ('24K Magic', artists[13], 2016),
        ('Planet Her', artists[14], 2021),
        ('Wonder', artists[15], 2020),
        ('Love Goes', artists[16], 2020),
        ('Montero', artists[17], 2021),
        ('Music of the Spheres', artists[18], 2021),
        ('Mercury - Act 1', artists[19], 2021),
        ('Folklore', artists[0], 2020),
        ('Equals', artists[1], 2021),
        ('Starboy', artists[3], 2016),
        ('Positions', artists[4], 2020),
        ('25', artists[6], 2015),
    ]
    
    albums = []
    for name, artist, year in albums_data:
        album = Album.objects.create(
            album_name=name,
            artist=artist,
            release_year=year
        )
        albums.append(album)
    
    print(f"✓ Created {len(albums)} albums")
    return albums

def create_songs(albums):
    """Create 60 songs"""
    print("\nCreating songs...")
    
    genres = ['Pop', 'Rock', 'Hip Hop', 'R&B', 'Electronic', 'Indie', 'Alternative']
    
    songs_data = [
        # Midnights
        ('Anti-Hero', albums[0], 200, 'Pop'),
        ('Lavender Haze', albums[0], 197, 'Pop'),
        ('Midnight Rain', albums[0], 174, 'Pop'),
        
        # Divide
        ('Shape of You', albums[1], 233, 'Pop'),
        ('Perfect', albums[1], 263, 'Pop'),
        ('Castle on the Hill', albums[1], 261, 'Pop'),
        
        # Happier Than Ever
        ('Happier Than Ever', albums[2], 298, 'Alternative'),
        ('my future', albums[2], 210, 'Indie'),
        ('Therefore I Am', albums[2], 174, 'Pop'),
        
        # After Hours
        ('Blinding Lights', albums[3], 200, 'R&B'),
        ('Save Your Tears', albums[3], 215, 'R&B'),
        ('In Your Eyes', albums[3], 237, 'R&B'),
        
        # Thank U, Next
        ('thank u, next', albums[4], 207, 'Pop'),
        ('7 rings', albums[4], 178, 'Pop'),
        ('break up with your girlfriend', albums[4], 190, 'Pop'),
        
        # Certified Lover Boy
        ('Way 2 Sexy', albums[5], 260, 'Hip Hop'),
        ('Girls Want Girls', albums[5], 244, 'Hip Hop'),
        ('Champagne Poetry', albums[5], 334, 'Hip Hop'),
        
        # 30
        ('Easy On Me', albums[6], 224, 'Pop'),
        ('Oh My God', albums[6], 225, 'Pop'),
        ('I Drink Wine', albums[6], 384, 'Pop'),
        
        # Hollywood's Bleeding
        ('Circles', albums[7], 215, 'Pop'),
        ('Sunflower', albums[7], 158, 'Pop'),
        ('Wow', albums[7], 149, 'Hip Hop'),
        
        # Future Nostalgia
        ('Don\'t Start Now', albums[8], 183, 'Pop'),
        ('Levitating', albums[8], 203, 'Pop'),
        ('Physical', albums[8], 193, 'Pop'),
        
        # Harry's House
        ('As It Was', albums[9], 167, 'Pop'),
        ('Music For a Sushi Restaurant', albums[9], 193, 'Pop'),
        ('Late Night Talking', albums[9], 177, 'Pop'),
        
        # SOUR
        ('good 4 u', albums[10], 178, 'Pop Rock'),
        ('drivers license', albums[10], 242, 'Pop'),
        ('deja vu', albums[10], 215, 'Pop'),
        
        # Un Verano Sin Ti
        ('Moscow Mule', albums[11], 243, 'Reggaeton'),
        ('Tití Me Preguntó', albums[11], 225, 'Reggaeton'),
        ('Yo No Soy Celoso', albums[11], 198, 'Reggaeton'),
        
        # Justice
        ('Peaches', albums[12], 198, 'Pop'),
        ('Ghost', albums[12], 153, 'Pop'),
        ('Anyone', albums[12], 210, 'Pop'),
        
        # 24K Magic
        ('24K Magic', albums[13], 226, 'Funk'),
        ('That\'s What I Like', albums[13], 206, 'R&B'),
        ('Finesse', albums[13], 217, 'Funk'),
        
        # Planet Her
        ('Kiss Me More', albums[14], 208, 'Pop'),
        ('Need to Know', albums[14], 210, 'Pop'),
        ('Woman', albums[14], 172, 'Pop'),
        
        # Wonder
        ('Wonder', albums[15], 202, 'Pop'),
        ('Monster', albums[15], 195, 'Pop'),
        ('305', albums[15], 212, 'Pop'),
        
        # Love Goes
        ('Diamonds', albums[16], 212, 'Pop'),
        ('My Oasis', albums[16], 182, 'Pop'),
        ('Kids Again', albums[16], 189, 'Pop'),
        
        # Montero
        ('MONTERO', albums[17], 137, 'Pop'),
        ('Industry Baby', albums[17], 212, 'Hip Hop'),
        ('That\'s What I Want', albums[17], 143, 'Pop'),
        
        # Music of the Spheres
        ('My Universe', albums[18], 228, 'Pop'),
        ('Higher Power', albums[18], 203, 'Pop'),
        ('Humankind', albums[18], 206, 'Pop'),
        
        # Mercury - Act 1
        ('Enemy', albums[19], 173, 'Rock'),
        ('Wrecked', albums[19], 249, 'Rock'),
        ('Follow You', albums[19], 189, 'Rock'),
        
        # Folklore
        ('cardigan', albums[20], 239, 'Indie'),
        ('exile', albums[20], 284, 'Indie'),
        ('the 1', albums[20], 210, 'Indie'),
        
        # Additional songs for variety
        ('Shivers', albums[21], 207, 'Pop'),
        ('Bad Habits', albums[21], 231, 'Pop'),
        ('Starboy', albums[22], 230, 'R&B'),
        ('positions', albums[23], 172, 'Pop'),
    ]
    
    songs = []
    for title, album, duration, genre in songs_data:
        song = Song.objects.create(
            title=title,
            album=album,
            duration=duration,
            genre=genre,
            file_link=f'/music/{title.lower().replace(" ", "_")}.mp3'
        )
        songs.append(song)
    
    print(f"✓ Created {len(songs)} songs")
    return songs

def create_playlists(users, songs):
    """Create 20 playlists"""
    print("\nCreating playlists...")
    
    playlist_names = [
        'Morning Coffee Vibes',
        'Evening Chill',
        'Workout Energy',
        'Study Focus',
        'Party Hits',
        'Road Trip Mix',
        'Relaxing Sundays',
        'Top Pop 2023',
        'Indie Favorites',
        'R&B Classics',
        'Dance Party',
        'Acoustic Sessions',
        'Feel Good Music',
        'Late Night Vibes',
        'Summer Anthems',
        'Rainy Day Mood',
        'Throwback Favorites',
        'New Discoveries',
        'Cafe Background',
        'Happy Tunes',
    ]
    
    playlists = []
    for i, name in enumerate(playlist_names):
        user = users[i % len(users)]
        playlist = Playlist.objects.create(
            playlist_name=name,
            user=user
        )
        
        # Add 5-10 random songs to each playlist
        num_songs = random.randint(5, 10)
        selected_songs = random.sample(songs, num_songs)
        
        for song in selected_songs:
            PlaylistSong.objects.create(playlist=playlist, song=song)
        
        playlists.append(playlist)
    
    print(f"✓ Created {len(playlists)} playlists with songs")
    return playlists

def create_play_history(users, songs):
    """Create 100 play history entries"""
    print("\nCreating play history...")
    
    history_entries = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(100):
        user = random.choice(users)
        song = random.choice(songs)
        played_at = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59)
        )
        
        entry = PlayHistory.objects.create(
            song=song,
            user=user,
            played_at=played_at
        )
        history_entries.append(entry)
    
    print(f"✓ Created {len(history_entries)} play history entries")
    return history_entries

def print_summary():
    """Print database summary"""
    print("\n" + "="*50)
    print("DATABASE SUMMARY")
    print("="*50)
    print(f"Users: {User.objects.count()}")
    print(f"Artists: {Artist.objects.count()}")
    print(f"Albums: {Album.objects.count()}")
    print(f"Songs: {Song.objects.count()}")
    print(f"Playlists: {Playlist.objects.count()}")
    print(f"Playlist Songs: {PlaylistSong.objects.count()}")
    print(f"Play History: {PlayHistory.objects.count()}")
    print("="*50)
    print("\n✅ Sample data added successfully!")
    print("\nYou can now:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/admin/")
    print("3. Login with your superuser credentials")
    print("4. Browse all the sample data!")

def main():
    print("Starting data seeding process...")
    print("="*50)
    
    # Clear existing data
    clear_existing_data()
    
    # Create data in order (respecting foreign key relationships)
    users = create_users()
    artists = create_artists()
    albums = create_albums(artists)
    songs = create_songs(albums)
    playlists = create_playlists(users, songs)
    play_history = create_play_history(users, songs)
    
    # Print summary
    print_summary()

if __name__ == '__main__':
    main()