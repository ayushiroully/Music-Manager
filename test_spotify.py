import time
import spotipy
import spotipy.util as util
from abstractClient import AbstractMusicClient
import schedule
import random
import datetime
import threading 


#global Variables
likedSongs = []
like_limit = 50 #User can only like 50 songs in 30 seconds
getLikedSongsLimit = 10000 #Spotify provided maximum 10000 songs for a particular user.
monitor_thread = True      #maximumLikeLimitinThreadTimeout = 2000
token_refresh_time = 3300 #Mention refresh time in seconds
monitor_thread_time = 30 

#userConfigforSpotify
defaultPlaylist = 'Synced Music'
client_id = '195046102e0d48e1b2abeeb16c333b1f'
client_secret = '5dc1c5461fe84971b9e378932efe004b'
redirect_uri = 'http://127.0.0.1:5000/'
url = 'https://accounts.spotify.com/authorize'
scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-follow-read' 
username = 'Vicarious11' #enter username here


def get_token():
	global token 
	token = util.prompt_for_user_token(username,scope,client_id,client_secret,redirect_uri)


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
				self.playlistID = playlist["id"]
				break
			else:		
				playlist = sp.user_playlist_create(userId,playlistName)
				self.playlistID = playlist["id"]
				break
		del sp

	def search_song(self, name, artist,search_limit):
		sp = spotipy.Spotify(auth=token)
		results = sp.search(q='artist:' + artist, type='artist')
		items = results['artists']['items']
		if len(items) > 0:
			for i in items:
				results = sp.artist_top_tracks(i["uri"])
				for track in results['tracks'][:search_limit]:
					if track['name'] == name:
						trackName = track['name']
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

	def dislike_song(self, song):
		sp = spotipy.Spotify(auth=token)
		results = sp.user_playlist_remove_all_occurrences_of_tracks(username,self.playlistID,[song.song_id])
		print(results)
		del sp

	def like_song(self, song):
		sp = spotipy.Spotify(auth=token)
		if song.song_id == "null":
			print("No song with that name present")
		results = sp.user_playlist_add_tracks(username,self.playlistID,[song.song_id])
		del sp 

#one time process. To be called before starting the monitor.
	def get_liked_songs(self):
		sp = spotipy.Spotify(auth=token)
		try:
			for i in range(0,getLikedSongsLimit, 50):	
				results = sp.current_user_saved_tracks(limit=50, offset=i)
				for item in results["items"]:
					track = item["track"]
					print(track["name"])
					likedSongs.append(track["name"])
					#sp.user_playlist_add_tracks(username,self.playlistID,[track["id"]])
		except TypeError:
			print("Songs Appended Successfully")
			pass	
		del sp

	def start_monitor_thread(self,instanceName):
		T1 = threading.Thread(target = instanceName.start_like_monitor)
		T1.start()
		print("Scanning Initiated")
		T1.join()

	def stop_monitor_thread(self):
		monitor_thread = False

	def start_like_monitor(self):
		while monitor_thread:
			recentlyLikedSongs = []
			songIds = []
			differenceBuffer = []
			sp = spotipy.Spotify(auth=token)
			results = sp.current_user_saved_tracks(limit=50)
			for item in results["items"]:
				track = item["track"]
				recentlyLikedSongs.append(track["name"])
				songIds.append(track["id"])

			differenceBuffer = list(set(recentlyLikedSongs) - set(likedSongs[:50]))
			print(len(differenceBuffer))
			print(differenceBuffer)

			if len(differenceBuffer) > 0:
				for i in range(len(differenceBuffer)):
					sp.user_playlist_add_tracks(username,self.playlistID,[songIds[i]])
					likedSongs.insert(0,differenceBuffer[i])
			del differenceBuffer,sp,recentlyLikedSongs,songIds
			time.sleep(monitor_thread_time)

			if monitor_thread == False:
				break

if __name__=='__main__':
				get_token()
				musicManager = spotifyClient()
				artist = 'Bea Miller'
				name = 'like that'
				search_limit = 10000
				musicManager.createNewPlaylist(defaultPlaylist)
				print('Playlist Created')
				musicManager.get_liked_songs()
				musicManager.start_monitor_thread(musicManager)
				schedule.every(55).minutes.do(get_token())
				while True:
					pass
        
        #musicManager.start_like_monitor()
        
