import time
import spotipy
import pylast
from spotipy.oauth2 import SpotifyOAuth
from typing import List

from src.config.config import config
from src.core.scrobbler import Scrobbler
from src.services.server import create_server
from src.utils.logger import setup_logging

class AutoScrobbler:
    def __init__(self):
        self.logger = setup_logging()
        self.spotify_client = self._setup_spotify()
        self.lastfm_network = self._setup_lastfm()
        self.scrobbler = Scrobbler(self.spotify_client, self.lastfm_network)
        
    def _setup_spotify(self) -> spotipy.Spotify:
        """Initialize Spotify client."""
        sp_oauth = SpotifyOAuth(
            client_id=config.spotify['client_id'],
            client_secret=config.spotify['client_secret'],
            redirect_uri=config.spotify['redirect_uri'],
            scope=config.spotify['scope']
            # cache_path='cache.txt'
        )
        return spotipy.Spotify(auth=sp_oauth.get_access_token(as_dict=False))

    def _setup_lastfm(self) -> pylast.LastFMNetwork:
        """Initialize Last.fm network."""
        return pylast.LastFMNetwork(
            api_key=config.lastfm['api_key'],
            api_secret=config.lastfm['api_secret'],
            username=config.lastfm['username'],
            password_hash=config.lastfm['password_hash']
        )

    def load_playlists(self, playlist_uris: List[str]) -> None:
        """Load tracks from multiple playlists."""
        self.logger.info(f"Starting to load {len(playlist_uris)} playlists...")
        for i, playlist_uri in enumerate(playlist_uris, 1):
            try:
                self.logger.info(f"Loading playlist {i}/{len(playlist_uris)}: {playlist_uri}")
                self.scrobbler.fetch_playlist_tracks(playlist_uri)
                self.logger.info(f"Successfully loaded playlist {playlist_uri}")
                time.sleep(60)  # Respect rate limits
            except Exception as e:
                self.logger.error(f"Failed to load playlist {playlist_uri}: {str(e)}")

    def run(self, playlist_uris: List[str]) -> None:
        """Run the auto scrobbler."""
        try:
            # Start the keep-alive server
            create_server()
            
            # Load initial playlist tracks
            self.load_playlists(playlist_uris)
            
            # Main scrobbling loop
            while True:
                try:
                    track = self.scrobbler.scrobble_random_track()
                    self.logger.info(f"Now playing: {track['track_name']} by {track['track_artist_name']}")
                    time.sleep(15)
                    
                except Exception as e:
                    self.logger.error(f"Error in scrobbling loop: {str(e)}")
                    time.sleep(3600)  # Wait an hour before retrying
                    
        except Exception as e:
            self.logger.critical(f"Critical error in main loop: {str(e)}")
            raise