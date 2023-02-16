import sys
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

# Spotify credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
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
        self.track_label = QLabel


               