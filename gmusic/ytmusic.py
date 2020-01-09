from abstract_client import AbstractMusicClient


class YTMusic(AbstractMusicClient):

    def search_song(self, name, artist):
        pass

    def get_song_details(self, song_id):
        pass

    def get_liked_songs(self):
        pass

    def like_song(self, song):
        pass

    def dislike_song(self, song):
        pass

    def start_like_monitor(self):
        pass

    def stop_like_monitor(self):
        pass

    def create_like_monitor_thread(self):
        pass

    def set_sync_server(self, server):
        pass