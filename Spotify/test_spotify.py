from __future__ import print_function
import time
import spotipy
from abstractClient import AbstractMusicClient
import song
from authToken import authCodeFlow
import math

#global Variables
like_limit = 50            #User can only like 50 songs in 30 seconds
getLikedSongsLimit = 10000 #Spotify provided maximum 10000 songs for a particular user.
monitor_thread = True      #maximumLikeLimitinThreadTimeout = 2000
token_refresh_time = 55    #Mention refresh time in minutes
monitor_thread_time = 1    #mention liked song thread in seconds
search_limit = 10000

#userConfigforSpotify
defaultPlaylist = 'Synced Music'
username = 'Vicarious11' #enter username here

class spotifyClient(AbstractMusicClient):	
	Token = authCodeFlow()
	token = Token.get_access_token()
	sp = spotipy.Spotify(auth=token)

#	spotipy.
	def __init__(self):
		self.playlistID = None
		self.likedSongs = []
		self.MonitorMode = True

	def createNewPlaylist(self,playlistName):	
		user = self.sp.current_user()
		userId = user['id']
		playlists = self.sp.user_playlists(user["id"])
		for playlist in playlists["items"]:
			if playlist['name'] == playlistName:
				self.playlistID = playlist["id"]
				break
			else:		
				playlist = self.sp.user_playlist_create(userId,playlistName)
				self.playlistID = playlist["id"]
				break

	def search_song(self, name, artist,search_limit):
		results = self.sp.search(q='artist:' + artist, type='artist')
		items = results['artists']['items']
		if len(items) > 0:
			for i in items:
				results = self.sp.artist_top_tracks(i["uri"])
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
						return songObj
		return None

#Audioanalysis of a particular Track. Save the track details to database
	def get_song_details(self,songId):
		print("fuck you ")

	def dislike_song(self, song):
		results = self.sp.user_playlist_remove_all_occurrences_of_tracks(username,self.playlistID,[song.song_id])
		print(results)
		

	def like_song(self, song):
		if song.song_id == "null":
			print("No song with that name present")
		else:
			self.sp.user_saved_tracks_add([song.song_id])

#one time process. To be called before starting the monitor to create the global playlist
	def get_global_playlist(self, copyPlaylist):
		for trackIndex in range(0,getLikedSongsLimit, 50):	
			results = self.sp.current_user_saved_tracks(limit=50, offset=trackIndex)
			for item in results["items"]:
				track = item["track"]
				self.likedSongs.append(track["id"])	
				if copyPlaylist:
					self.sp.user_playlist_add_tracks(username,self.playlistID,[track["id"]])
				
			if results["next"] == None:
				break
         
	def get_liked_songs(self):
		recentlyLikedSongs = []
		for  trackIndex in range(0,getLikedSongsLimit, 50):
			results = self.sp.current_user_saved_tracks(limit=50,offset = trackIndex)
			for item in results["items"]:
				track = item["track"]
				recentlyLikedSongs.append(track["id"])

			if results["next"] == None:
				break

		return recentlyLikedSongs

	def start_like_monitor(self):
		self.MonitorMode = True

	def stop_like_monitor(self):
		self.MonitorMode = False


	def create_like_monitor_thread(self):
		count = 0 
		while self.MonitorMode:
			recentlyLikedSongs = []
			likeBuffer = []
			dislikeBuffer = []
			recentlyLikedSongs = self.get_liked_songs()

			likeBuffer    = list(set(recentlyLikedSongs) - set(self.likedSongs))
			dislikeBuffer = list(set(self.likedSongs) - set(recentlyLikedSongs))


			if len(likeBuffer) > 0:
				for trackId in likeBuffer:
					self.sp.user_playlist_add_tracks(username,self.playlistID,[trackId])
					self.likedSongs.insert(0,trackId)

			if len(dislikeBuffer) > 0:
				for trackId in dislikeBuffer:
					self.sp.user_playlist_remove_all_occurrences_of_tracks(username,self.playlistID,[trackId])
					self.likedSongs = [songId for songId in self.likedSongs if songId != trackId]

			print(likeBuffer)
			print(dislikeBuffer)
				
			del recentlyLikedSongs,likeBuffer, dislikeBuffer
			count = count + 1

			if count == int(math.floor(token_refresh_time / monitor_thread_time)):
				self.Token.refresh_token(self.sp)
				count = 0

			print(count)

			time.sleep(monitor_thread_time * 60)

musicManager = spotifyClient()
musicManager.createNewPlaylist(defaultPlaylist)
print("Playlist Created")
musicManager.get_global_playlist(False)
musicManager.start_like_monitor()
musicManager.create_like_monitor_thread()



