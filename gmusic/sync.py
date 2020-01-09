class SyncServer:
    def __init__(self, gmusic_client, spotify_client):
        self.gmusic_client = gmusic_client
        self.spotify_client = spotify_client

    def sync(self, source, song, action):
        if source == 'spotify':
            song = self.gmusic_client.search_song(song.name, song.artist)
            self.take_action_gmusic(song, action)
        elif source == 'gmusic':
            pass
            # song = self.spotify_client.search_song(song.name, song.artist)
            # self.take_action_spotify(song, action)

    def take_action_gmusic(self, song, action):
        if action == 'like':
            self.gmusic_client.like_song(song)
        elif action == 'dislike':
            self.gmusic_client.dislike_song(song)

    def take_action_spotify(self, song, action):
        if action == 'like':
            self.spotify_client.like_song(song)
        elif action == 'dislike':
            self.spotify_client.dislike_song(song)
