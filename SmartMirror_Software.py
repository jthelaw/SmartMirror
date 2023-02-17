import sys
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

# Spotify credentials
SPOTIPY_CLIENT_ID = 'your id'
SPOTIPY_CLIENT_SECRET = 'your secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'



class SmartMirror:
    def __init__(self):
        #Initialize spotipy client
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI))
        # Create the GUI
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle('Smart Mirror')
        self.window.setGeometry(200, 200, 600, 400)

        #Labels for the weather 
        self.weather_label = QLabel(self.window)
        self.weather_label.move(50, 50)
        self.weather_label.setFont(QFont('Arial', 20))

        #Label for current song(track)
        self.track_label = QLabel(self.window)
        self.track_label.move(50,100)
        self.track_label.setFont(QFont('Arial', 20))

        #Play/Pause button 
        self.play_button = QPushButton('Play', self.window)
        self.play_button.move(50,150)
        self.play_button.clicked.connect(self.spotify_play_pause)

        # Start event loop
        self.update_gui()
        self.window.show()
        self.exit(self.app.exec_())

    def update_gui(self):
        #updateing weather and current track labels
        weather = self.get_weather()
        self.weather_label.setText(f'Temperature: {weather["temp"]}°C\nDescription: {weather["description"]}')

        track = self.get_current_track()
        self.track_label.setText(track)

        # Schedule the next GUI update in 5 secs
        QTimer.singleShot(5000,self.update_gui)

    def get_weather(self):
        # Make a request to the OpenWeatherMap API
        weather_api_key = '08c62c95f2bcce8be869936907a2978c'
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?q=New%20York&appid={weather_api_key}&units=metric'
        response = requests.get(weather_url)
        data = json.loads(response.text)

        # Extract the relevant data from the response
        weather_data = {
            'temp': int(data['main']['temp']),
            'description': data['weather'][0]['description']
        }

        return weather_data
    
    def get_current_track(self):
        # Get the user's currently playing track from Spotify
        track = self.sp.current_playback()
        if track is None:
            return 'No track currently playing'
        else:
            track_name = track['item']['name']
            track_artist = track['item']['artists'][0]['name']
            return f'Now playing: {track_name} by {track_artist}'

    def spotify_play_pause(self):
        # Play/pause the user's Spotify account
        track = self.sp.current_playback()
        if track is None:
            self.sp.start_playback()
            self.play_button.setText('Pause')
        else:
            self.sp.pause_playback()
            self.play_button.setText('Play')

if __name__ == '__main__':
    SmartMirror()


    




               