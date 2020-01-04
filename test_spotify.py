import time
import spotipy
import spotipy.util as util
from abstractClient import AbstractMusicClient
import random
import datetime

#Global Config for connecting Auth Token.
client_id = '195046102e0d48e1b2abeeb16c333b1f'
client_secret = '5dc1c5461fe84971b9e378932efe004b'
redirect_uri = 'http://127.0.0.1:5000/'
url = 'https://accounts.spotify.com/authorize'
scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-follow-read' # ugc-image-upload' this is needed for uploading a custom image to the playlist
username = 'Vicarious11' #enter username here
defaultPlaylist = 'Synced Music'
token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)
likedSongs = []
getLikedSongsLimit = 10000 
#Spotify provided maximum 10000 songs for a particular user.

#maximumLikeLimitinThreadTimeout = 2000


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
		self.playlistID = None
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

#Audioanalysis of a particular Track. Save the track details to database
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

#one time process. To be called before starting the monitor.
	def get_liked_songs(self,playlistId):
		sp = spotipy.Spotify(auth=token)
		try:
			for i in range(0,getLikedSongsLimit, 50):	
				results = sp.current_user_saved_tracks(limit=50, offset=i)
				for item in results["items"]:
					track = item["track"]
					print(track["name"])
					likedSongs.append(track["name"])
					#sp.user_playlist_add_tracks(username,playlistId,[track["id"]])
		except TypeError:
			print("Songs Appended Successfully")
			pass	
		del sp

	def start_like_monitor(self,playlistId):
		recentlyLikedSongs = []
		songIds = []
		differenceBuffer = []
		sp = spotipy.Spotify(auth=token)
		results = sp.current_user_saved_tracks(limit=50)
		for item in results["items"]:
			track = item["track"]
			recentlyLikedSongs.append(track["name"])
			songIds.append(track["id"])
		differenceBuffer = set(recentlyLikedSongs) - set(likedSongs[:50])
		likedSongs.extend(differenceBuffer)
		print(differenceBuffer)
		print("lets see if there are any liked songs until then")
		if len(differenceBuffer) > 0:
			for i in range(0,len(differenceBuffer)):
				sp.user_playlist_add_tracks(username,playlistId,[songIds['i']])
				print("I am Sexy and I know it")
		del sp

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
        musicManager.get_liked_songs(playlistId)
        musicManager.start_like_monitor(playlistId)

