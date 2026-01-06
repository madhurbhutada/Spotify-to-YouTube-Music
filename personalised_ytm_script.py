# open source workaround
from ytmusicapi import setup_oauth, YTMusic
import json
import os
import sys
import platform
import subprocess
import time

# ytmigrate/
# ├── spotify_data.json            
# ├── migrate.py                   # core migration logic
# ├── run_windows.cmd              # Windows launcher
# ├── run_macos.command            # macOS launcher
# ├── runtimes/
# │   ├── windows/
# │   │   └── python/
# │   │       └── python.exe
# │   └── macos/
# │       └── python/
# │           └── bin/python3
# ├── logs/                         # created at runtime
# └── README.md

def send_script_data(complete_user_migration_data):
    global spotify_data 
    spotify_data = json.loads(complete_user_migration_data)
    return

def ensure_ytmusic_oauth():
    try:
        ytmusic = YTMusic("oauth.json")
    except FileNotFoundError:
        # Interactive login
        setup_oauth("oauth.json", open_browser=True)
        ytmusic = YTMusic("oauth.json")

    return ytmusic

def get_tracks():
    YTMusic.search

def create_playlists():
    YTMusic.create_playlist
    # also returns the playlist ID
    # store the ID for future usage

def update_playlists():
    YTMusic.add_playlist_items

def main():
    ytmusic = ensure_ytmusic_oauth()

if __name__ == "__main__":
    main()
