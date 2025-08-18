from src.core.app import AutoScrobbler

# List of Spotify playlists
PLAYLIST_URIS = [
    '2gYEFpujTykvXW3InbWJRk',  # Global Hot 100™
    # '3uMnOgaB96EuIuywzTTJrW',  # Billie Eilish x 100™
    # '7x0UmJkmyV71SukHU5dzzM',  # The Weeknd x 100™
    # Add more playlists as needed
]

def main():
    """Main entry point for the Auto Scrobbler application."""
    try:
        app = AutoScrobbler()
        app.run(PLAYLIST_URIS)
    except Exception as e:
        print(f"Application crashed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
