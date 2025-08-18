import os
import pylast
from dotenv import load_dotenv

class Config:
    def __init__(self):
        load_dotenv()
        
        # Spotify Configuration
        self.spotify = {
            'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
            'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
            'redirect_uri': 'http://localhost:9005',
            'scope': 'user-library-read playlist-read-private playlist-read-collaborative user-read-currently-playing'
        }
        
        # Last.fm Configuration
        password = os.getenv('LASTFM_PASSWORD')
        self.lastfm = {
            'api_key': os.getenv('LASTFM_API_KEY'),
            'api_secret': os.getenv('LASTFM_API_SECRET'),
            'username': os.getenv('LASTFM_USERNAME'),
            'password_hash': pylast.md5(password) if password else None
        }
        
        # Server Configuration
        self.server = {
            'host': '0.0.0.0',
            'port': 3125
        }
        
        # Logging Configuration
        self.logging = {
            'file': 'logs/auto_scrobble.log',
            'level': 'ERROR'
        }

config = Config()