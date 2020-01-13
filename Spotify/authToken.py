import spotipy.oauth2 as oauth2

client_id = '195046102e0d48e1b2abeeb16c333b1f'
client_secret = '5dc1c5461fe84971b9e378932efe004b'
redirect_uri = 'http://127.0.0.1:5000/'
url = 'https://accounts.spotify.com/authorize'
scope = 'user-library-read user-top-read playlist-modify-public playlist-modify-private user-follow-read' 

class authCodeFlow:
	sp_oauth = oauth2.SpotifyOAuth(client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri,scope=scope)
	token_info = sp_oauth.get_cached_token() 	
	def __init__(self):
		pass

	def get_access_token(self):	
		if not self.token_info:
			auth_url = self.sp_oauth.get_authorize_url()
			print(auth_url)
			response = input('Paste the above link into your browser, then paste the redirect url here: ')
			code = self.sp_oauth.parse_response_code(response)
			self.token_info = self.sp_oauth.get_access_token(code)
			token = self.token_info['access_token']	
		return token

	def refresh_token(self, instance):
		
		self.token_info = self.sp_oauth.refresh_access_token(self.token_info['refresh_token'])
		token = self.token_info['access_token']
		print(token)
		print("Its refreshed")
		instance = spotipy.Spotify(auth=token)