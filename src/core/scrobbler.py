import random
import time
import logging
from typing import Dict, List

class Scrobbler:
    def __init__(self, spotify_client, lastfm_network):
        self.spotify = spotify_client
        self.network = lastfm_network
        self.tracks_cache: List[Dict] = []
        self.logger = logging.getLogger(__name__)

    def fetch_playlist_tracks(self, playlist_id: str, limit: int = 10) -> None:
        """Fetch tracks from a playlist and add them to the cache."""
        try:
            playlist_tracks = self.spotify.playlist_tracks(f'spotify:playlist:{playlist_id}', limit=limit, offset=0)
            for track in playlist_tracks['items']:
                track_info = self._extract_track_info(track)
                if track_info:
                    self.tracks_cache.append(track_info)
        except Exception as e:
            self.logger.error(f"Error fetching playlist tracks: {str(e)}")
            raise

    def _extract_track_info(self, track: Dict) -> Dict:
        """Extract relevant track information from Spotify track object."""
        try:
            track_data = track['track']
            album_details = self.spotify.album(track_data['album']['id'])
            
            return {
                'track_name': track_data['name'],
                'track_artist_name': track_data['artists'][0]['name'],
                'album_name': album_details['name'],
                'track_id': track_data['id']
            }
        except Exception as e:
            self.logger.error(f"Error extracting track info: {str(e)}")
            return None

    def scrobble_random_track(self) -> None:
        """Scrobble a random track from the cache."""
        if not self.tracks_cache:
            raise ValueError("No tracks in cache")

        track = random.choice(self.tracks_cache)
        try:
            # self.logger.info(f"Preparing to scrobble: {track['track_name']} by {track['track_artist_name']}")
            
            # Update now playing
            self.network.update_now_playing(
                artist=track['track_artist_name'],
                title=track['track_name'],
                album=track['album_name']
            )
            self.logger.info("Updated now playing status")

            # Scrobble the track
            self.network.scrobble(
                artist=track['track_artist_name'],
                title=track['track_name'],
                timestamp=int(time.time()),
                album=track['album_name']
            )
            self.logger.info("Track scrobbled successfully")

            # Randomly love/unlove tracks
            self._handle_track_love(track)

            # self.logger.info(f"Completed processing: {track['track_name']} by {track['track_artist_name']}")
            return track

        except Exception as e:
            self.logger.error(f"Error scrobbling track: {str(e)}")
            raise

    def _handle_track_love(self, track: Dict) -> None:
        """Randomly love or unlove a track."""
        try:
            track_obj = self.network.get_track(
                artist=track['track_artist_name'],
                title=track['track_name']
            )

            if random.random() > 0.4999:
                track_obj.love()
                self.logger.info(f"Loved track: {track['track_name']}")
            else:
                track_obj.unlove()
                self.logger.info(f"Unloved track: {track['track_name']}")

        except Exception as e:
            self.logger.error(f"Error handling track love: {str(e)}")