from abc import ABC, abstractmethod


class AbstractMusicClient(ABC):
    MONITOR_MODE = True
    liked_songs = []
    sync_server_callback = None

    def __init__(self):
        super(AbstractMusicClient, self).__init__()

    @abstractmethod
    def search_song(self, name, artist):
        pass

    @abstractmethod
    def get_song_details(self, song_id):
        pass

    @abstractmethod
    def get_liked_songs(self):
        pass

    @abstractmethod
    def like_song(self, song):
        pass

    @abstractmethod
    def dislike_song(self, song):
        pass

    @abstractmethod
    def start_like_monitor(self):
        pass

    @abstractmethod
    def stop_like_monitor(self):
        pass

    @abstractmethod
    def create_like_monitor_thread(self):
        pass

    @abstractmethod
    def set_sync_server(self, server):
        pass
