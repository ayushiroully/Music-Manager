from abstract_client import AbstractMusicClient
from gmusicapi import Mobileclient
from song import Song
import threading
import time


class GMusic(AbstractMusicClient):
    client = Mobileclient()

    def __init__(self, server):
        self.set_sync_server(server)
        super().__init__()

    def oauth(self):
        self.client.perform_oauth()

    def login(self):
        self.client.oauth_login(Mobileclient.FROM_MAC_ADDRESS)
        self.start_like_monitor()

    def logout(self):
        self.client.logout()
        self.stop_like_monitor()
        self.liked_songs = []

    def search_song(self, name, artist):
        query = '%s %s' % (name, artist)
        search_results = self.client.search(query, 10)
        if len(search_results['song_hits']):
            tmp_song = search_results['song_hits'][0]['track']
            google_id = tmp_song['nid']
            name = tmp_song['title']
            artist = tmp_song['artist']
            album = tmp_song['album']
            track_type = tmp_song['trackType']
            song_obj = Song('', google_id, name, artist, album, track_type)
            return song_obj
        return None

    def get_all_playlists(self):
        return self.client.get_all_playlists()

    def get_song_details(self, song_id):
        return self.client.get_track_info(song_id)

    def get_liked_songs(self):
        return self.client.get_promoted_songs()

    def like_song(self, song):
        google_song = self.search_song(song.name, song.artist)
        new_song = Song(song.song_id, google_song.google_id, song.name, song.artist, song.album, google_song.track_type)
        self.client.rate_songs([{'nid': new_song.google_id, 'trackType': new_song.track_type}], 5)

    def dislike_song(self, song):
        google_song = self.search_song(song.name, song.artist)
        new_song = Song(song.song_id, google_song.google_id, song.name, song.artist, song.album, google_song.track_type)
        self.client.rate_songs([{'nid': new_song.google_id, 'trackType': new_song.track_type}], 1)

    def start_like_monitor(self):
        monitor_thread = threading.Thread(target=self.create_like_monitor_thread, daemon=True)
        monitor_thread.start()

    def stop_like_monitor(self):
        self.MONITOR_MODE = False

    def create_like_monitor_thread(self):
        while self.MONITOR_MODE:
            tmp_liked_songs = self.get_liked_songs()

            tmp_liked_song_ids = set([song['nid'] for song in tmp_liked_songs])
            liked_song_ids = set([song.google_id for song in self.liked_songs])

            new_liked_song_ids = tmp_liked_song_ids.difference(liked_song_ids)
            disliked_song_ids = liked_song_ids.difference(tmp_liked_song_ids)

            tmp_songs_dict = dict((song.google_id, song) for song in self.liked_songs)
            self.liked_songs.clear()
            new_liked_songs = []
            disliked_songs = []

            for tmp_song_id in disliked_song_ids:
                disliked_songs.append(tmp_songs_dict[tmp_song_id])
                self.sync_server_callback('gmusic', tmp_songs_dict[tmp_song_id], 'dislike')

            for tmp_song in tmp_liked_songs:
                google_id = tmp_song['nid']
                name = tmp_song['title']
                artist = tmp_song['artist']
                album = tmp_song['album']
                track_type = tmp_song['trackType']
                song_obj = Song('', google_id, name, artist, album, track_type)
                if google_id in new_liked_song_ids:
                    new_liked_songs.append(song_obj)
                    self.sync_server_callback('gmusic', song_obj, 'like')
                self.liked_songs.append(song_obj)
            time.sleep(30)

    def set_sync_server(self, server):
        self.sync_server_callback = server
