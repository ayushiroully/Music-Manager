import time
import spotipy
import spotipy.util as util
from abstractClient import AbstractMusicClient
import random
import datetime


client_id = '195046102e0d48e1b2abeeb16c333b1f'
client_secret = '5dc1c5461fe84971b9e378932efe004b'
redirect_uri = 'http://127.0.0.1:5000/'
url = 'https://accounts.spotify.com/authorize'
scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-follow-read' # ugc-image-upload' this is needed for uploading a custom image to the playlist
username = 'Vicarious11' #enter username here
defaultPlaylist = 'Synced Music'
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
likedSongs = []


class song:
	def __init__(self, spotify_id, google_id, name, artist, album, track_type):
		self.song_id = spotify_id
		self.google_id = google_id
		self.name = name
		self.artist = artist
		self.album = album
		self.track_type = track_type

class spotifyClient(AbstractMusicClient):
	def __init__(self):
		pass

	def createNewPlaylist(self,playlistName):	
		sp = spotipy.Spotify(auth=token)
		user = sp.current_user()
		userId = user['id']
		playlists = sp.user_playlists(user["id"])
		for playlist in playlists["items"]:
			if playlist['name'] == playlistName:
				return playlist["id"]
			else:		
				playlist = sp.user_playlist_create(userId,playlistName)
				del sp
				return playlist["id"]
	
	def search_song(self, name, artist,search_limit):
		sp = spotipy.Spotify(auth=token)
		results = sp.search(q='artist:' + artist, type='artist')
		items = results['artists']['items']
		if len(items) > 0:
			for i in items:
				results = sp.artist_top_tracks(i["uri"])
				for track in results['tracks'][:search_limit]:
					if track['name'] == name:
						trackName =track['name']
						artistName = i["name"]
						albumName = track['album'].get("name","none")
						spotify_id = track["id"]
						print(track["id"])
						google_id = ""
						track_type = ""
						songObj = song(spotify_id,google_id,trackName,artistName,albumName,track_type)
						print(songObj)
						del sp
						return songObj
		del sp
		return None
	
	def get_song_details(self,songId):
		print("fuck")

	def dislike_song(self, song,playlistId):
		sp = spotipy.Spotify(auth=token)
		results = sp.user_playlist_remove_all_occurrences_of_tracks(username,playlistId,[song.song_id])
		print(results)
		del sp

	def like_song(self, song, playlistId):
		sp = spotipy.Spotify(auth=token)
		if song.song_id == "null":
			print("No song with that name present")
		results = sp.user_playlist_add_tracks(username,playlistId,[song.song_id])
		del sp 

	def start_like_monitor(self,playlistId):
		sp = spotipy.Spotify(auth=token)
		for i in range(0,50):
			results = sp.current_user_saved_tracks(limit=50, offset=i)
			for item in results["items"]:
				track = item["track"]
				likedSongs.append(track["name"])
				results = sp.user_playlist_add_tracks(username,playlistId,[track["id"]])
		del sp
		print(len(likedSongs))

if __name__=='__main__':
        musicManager = spotifyClient()
        artist = 'Bea Miller'
        name = 'like that'
        search_limit = 10000
        playlistId = musicManager.createNewPlaylist(defaultPlaylist)
        print('Playlist Created')
       	searchedSong = musicManager.search_song(name,artist,search_limit)
        if searchedSong == None:
        	print("Song not found")
        else:
        	musicManager.like_song(searchedSong, playlistId)
        print("Song Added")
        musicManager.dislike_song(searchedSong, playlistId)
        print("Song Deleted")
        musicManager.start_like_monitor(playlistId)

