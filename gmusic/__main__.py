from gmusic import GMusic
from sync import SyncServer


class FuckTheHack:

    def __init__(self):
        # Clients init.
        gmusic_client = GMusic(self.sync_clients)
        gmusic_client.login()
        spotify_client = None

        # Sync server init
        self.sync_server = SyncServer(gmusic_client, spotify_client)

    def sync_clients(self, source, song, action):
        self.sync_server.sync(source, song, action)


if __name__ == '__main__':
    FuckTheHack()
    input('Exit?')
