import sys
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PyQt5.QtWidgets import  QApplication, QLabel, QPushButton, QWidget, QInputDialog, QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer
import tkinter as tk

# Spotify credentials
SPOTIPY_CLIENT_ID = 'your CLIENT_ID '
SPOTIPY_CLIENT_SECRET = 'Your CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'http://localhost:8000/callback'



class SmartMirror:
    def __init__(self):
        # Initialize the Pytify library and authenticate with Spotify
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                client_secret=SPOTIPY_CLIENT_SECRET,
                                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                                scope='user-read-playback-state,user-modify-playback-state,user-library-read'))

        # Create the GUI
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle('Smart Mirror')
        self.window.setGeometry(200, 200, 600, 400)

        # Create labels for the weather and current track
        self.weather_label = QLabel(self.window)
        self.weather_label.setFont(QFont('Roboto', 18))
        self.weather_label.setStyleSheet('color: black;')
        
        self.track_label = QLabel(self.window)
        self.track_label.move(1, 100)
        self.track_label.setFont(QFont('Arial', 20))

         # Add separate buttons for play and pause
        self.play_button = QPushButton(self.window)
        self.play_button.setIcon(QIcon('play.png'))
        self.play_button.move(50, 150)
        self.play_button.clicked.connect(self.spotify_play)

        self.pause_button = QPushButton(self.window)
        self.pause_button.setIcon(QIcon('pause.png'))
        self.pause_button.move(150, 150)
        self.pause_button.clicked.connect(self.spotify_pause)


        #search button
        self.search_button = QPushButton('Search', self.window)
        self.search_button.move(200, 150)
        self.search_button.clicked.connect(self.search_spotify)

        # Start the event loop
        self.update_gui()
        self.window.show()
        sys.exit(self.app.exec_())
    
    

    def update_gui(self):
        # Update the weather and current track labels
        weather = self.get_weather()
        self.weather_label.setText(f'Temperature: {weather["temp"]}°C\n{weather["description"]}')

        track = self.get_current_track()
        self.track_label.setText(track)

        # Schedule the next GUI update in 5 seconds
        QTimer.singleShot(5000, self.update_gui)

    def get_weather(self):
        # Make a request to the Weatherbit API
        location = 'Burnsville,MN'
        api_key = 'Your api_key'
        weather_url = f'https://api.weatherbit.io/v2.0/current?city={location}&key={api_key}&units=M'
        response = requests.get(weather_url)
        data = json.loads(response.text)

        # Extract the relevant data from the response
        weather_data = {
            'temp': int(data['data'][0]['temp']),
            'description': data['data'][0]['weather']['description']
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

    def spotify_play(self):
        # Play the user's Spotify account
        self.sp.start_playback()
        self.play_button.hide()
        self.pause_button.show()
    
    def spotify_pause(self):
        # Pause the user's Spotify account
        self.sp.pause_playback()
        self.pause_button.hide()
        self.play_button.show()
    
    def search_spotify(self):
    # Get the user's liked songs from Spotify
        offset = 0
        limit = 50
        liked_songs = []
        while True:
            results = self.sp.current_user_saved_tracks(offset=offset, limit=limit)
            if not results['items']:
                break
            for item in results['items']:
                track = item['track']
                track_name = track['name']
                track_artist = track['artists'][0]['name']
                liked_songs.append(f'{track_name} by {track_artist}')
            offset += limit

        # Prompt the user to enter a search query
        query, ok = QInputDialog.getText(self.window, 'Search for a song', 'Enter a song name:')
        if ok:
            # Search for the song on Spotify
            search_results = self.sp.search(q=query, type='track', limit=1)
            if search_results['tracks']['items']:
                track_uri = search_results['tracks']['items'][0]['uri']
                self.sp.start_playback(uris=[track_uri])
                self.track_label.setText(f'Now playing: {search_results["tracks"]["items"][0]["name"]} by {search_results["tracks"]["items"][0]["artists"][0]["name"]}')
                self.play_button.setText('Pause')
            else:
                QMessageBox.warning(self.window, 'Song not found', 'Sorry, the song could not be found.')


if __name__ == '__main__':
    SmartMirror()
    




               