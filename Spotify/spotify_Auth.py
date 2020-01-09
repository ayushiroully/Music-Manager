import spotipy,sys,os,json,webbrowser,re
import spotipy.util as util

from json.decoder import JSONDecodeError

class fuck_the_hack():
    def __init__(self):
        self.scope = 'user-read-playback-state user-read-currently-playing'
        self.username = "AyushiRoully" 
        self.client_id = "4eb167275081428b8f8ee26b52ea3852"
        self.client_secret = "afa6f8a49c9c4c1a8547482d5e6aee0e"
        self.redirect_uri = "http://127.0.0.1:5000/"
        #username = sys.argv[1]
        #userid = 31naotuyob6n4od4ii2iuswezvdu

        try:
            self.token = util.prompt_for_user_token(self.username,self.scope,self.client_id,self.client_secret,self.redirect_uri)
        except (AttributeError,JSONDecodeError):
            os.remove(f".cache-{self.username}")
            self.token = util.prompt_for_user_token(self.username,self.scope,self.client_id,self.client_secret,self.redirect_uri)
    
        self.sp = spotipy.Spotify(auth=self.token)

    final_data = {}
    
    def user_data(self):
        #get user data
        user = self.sp.current_user()
        name = json.dumps(user['display_name'],sort_keys=True,indent= 4)
        return name 
    
    def active_device(self):    
        #get users device name and deviceId
        device = self.sp.devices()
        device_data = {}
        device = device["devices"]
        for i in device:
            deviceId = i.get('id')
            device_name = i.get('name') 
        device_data = {"id" : deviceId, "device_name" : device_name}
        return device_data
            

    def track_data(self):
        #get curent playing track details
        track = {}
        current_track = self.sp.b()
        #time of playing track
        play_time = current_track["timestamp"]
        track_details = current_track["item"]
        #name and spotify Id of track
        song_name = track_details["name"]
        song_id = track_details['id']
        track = {"play_time" : play_time,"track_name" :song_name,"track_id": song_id}
        return track
        
    
    def final_value(self):
    # a = fuck_the_hack
        user_details = self.user_data()
        device_active = self.active_device()
        track_d = self.track_data()
        final_data = {"User name:": user_details,"device": device_active,"track_name" : track_d}
        return final_data
        
if __name__ == "__main__":
    a = fuck_the_hack()
    print(a.final_value())
    

