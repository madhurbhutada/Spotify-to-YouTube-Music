# sp-ytm-migrate/
# ├── spotify_data.json          # fetched
# ├── migrate.py                 # core logic
# ├── run_windows.cmd
# ├── run_macos.command
# ├── runtime_templates/
# │   ├── windows/
# │   │     ├── python/
# │   │     │    └── python.exe
# │   │     └── site-packages/
# │   │          └── ytmusicapi/
# │   └── macos/
# │         ├── python/
# │         │   └── bin/python3
# │         └── site-packages/
# │             └── ytmusicapi/
# ├── migration_logs.log                      # created at runtime
# └── README.txt

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "runtime_templates/windows/site-packages"))

from ytmusicapi import YTMusic

import json
import os
import webbrowser
import random
import time
import logging

LOG_DIR = Path(__file__).resolve().parent

LOG_FILE = LOG_DIR / "migration_logs.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.getLogger("ytmusicapi").setLevel(logging.WARNING)

logger = logging.getLogger("ytmigrate")

logger.info("Python version: %s", sys.version)
logger.info("Platform: %s", sys.platform)
logger.info("Base directory: %s", BASE)

SPOTIFY_JSON = BASE / "spotify_data.json"
BROWSER_FILE = BASE / "browser.json"
DELAY_CONST_LOW = 0.5
DELAY_CONST_HIGH = 1.5
PLAYLIST_CREATION_DELAY = 5.0  # Longer delay between playlist creations

def load_spotify_data():
    if not os.path.exists(SPOTIFY_JSON):
        raise FileNotFoundError(f"{SPOTIFY_JSON} not found")
    
    logger.info("Spotify JSON path: %s", SPOTIFY_JSON)

    with open(SPOTIFY_JSON, "r", encoding="utf8") as f:
        return json.load(f)

def parse_header(header_str):
    try:
        start_marker = '"headers":'
        start_index = header_str.find(start_marker)

        if start_index == -1:
            try:
                return json.loads(header_str)
            except:
                logger.exception("Could not find 'headers' object in input.")
                sys.exit(1)

        open_brace_index = header_str.find('{', start_index)
        if open_brace_index == -1:
            raise ValueError("Found 'headers' but no opening brace.")

        brace_count = 0
        end_index = -1

        for i in range(open_brace_index, len(header_str)):
            char = header_str[i]
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
            
            if brace_count == 0:
                end_index = i + 1
                break
        
        if end_index == -1:
            raise ValueError("Malformed JSON: Could not find closing brace.")

        json_text = header_str[open_brace_index:end_index]
        
        parsed_header = json.loads(json_text)
        return parsed_header

    except Exception as e:
        logger.exception("Failed to parse headers")
        sys.exit(1)

def take_multiline_input():
    lines = []
    try:
        while True:
            line = input()
            lines.append(line)
    except EOFError:
        pass

    return "\n".join(lines)

def ensure_ytmusic_auth():
    if os.path.exists(BROWSER_FILE):
        try:
            logger.info("Using existing YouTube Music browser authentication...")
            return YTMusic(str(BROWSER_FILE))
        except Exception:
            logger.exception("Existing file invalid. Re-authentication needed.")
            os.remove(BROWSER_FILE)

    logger.info("1. YouTube Music authentication required (one-time setup).")
    print("2. Your data does NOT leave your device.")
    print("3. This is not stored and do not share this with anyone.\n")
    input("Press Enter to open YouTube Music in your browser...")

    webbrowser.open("https://music.youtube.com")

    print("\nMake sure you're logged in on Edge/Chrome/Brave!\nInstructions:")
    print("1. Open DevTools (Ctrl+Shift+I / Cmd+Option+I)")
    print("2. Go to Network tab")
    print("3. Click Library")
    print("4. Find request starting with 'browse?'")
    print("5. Copy → Copy as fetch (Node.js)")
    print("6. Paste, Enter, then Ctrl+Z + Enter (Windows) or Ctrl+D")

    header_str = take_multiline_input()
    headers_dict = parse_header(header_str)

    try:
        cookie_val = next(
            (v for k, v in headers_dict.items() if k.lower() == "cookie"),
            None
        )

        if not cookie_val or "SAPISID=" not in cookie_val:
            raise ValueError("SAPISID cookie missing. Are you logged in?")

        with open(BROWSER_FILE, "w", encoding="utf-8") as f:
            json.dump(headers_dict, f, indent=2)

        logger.info("Authentication saved successfully.")
        return YTMusic(str(BROWSER_FILE))

    except Exception:
        logger.exception("Authentication failed")
        sys.exit(1)

def normalize_artists(artists):
    if isinstance(artists, list):
        return ", ".join(artists)
    return artists or ""

def get_video_ids(ytmusic, tracks):
    video_ids = []

    for idx, track in enumerate(tracks, start=1):
        name = track.get("name")
        artists = normalize_artists(track.get("artists"))

        if not name:
            logger.info(f"[{idx}] Skipping track with no name")
            continue

        query = f"{name} by {artists}".strip()
        logger.info(f"[{idx}/{len(tracks)}] Searching: {query}")

        try:
            results = ytmusic.search(query=query, filter="songs", limit=1)

            if results and len(results) > 0:
                best = results[0]
                video_ids.append(best["videoId"])
                logger.info(f"   -> Found: {best.get('title')} ({best.get('videoId')})")
            else:
                logger.info("   -> Song not found, trying video search...")
                results = ytmusic.search(query=query, filter="videos", limit=1)
                if results and len(results) > 0:
                    best = results[0]
                    video_ids.append(best["videoId"])
                    logger.info(f"   -> Found Video: {best.get('title')}")
                else:
                    logger.info("   -> No match found.")

        except Exception as e:
            logger.exception("Search error")

        time.sleep(
            DELAY_CONST_LOW 
            + random.random() 
            * DELAY_CONST_HIGH
        )

    return video_ids, len(video_ids)

def map_privacy(value):
    allowed = {"PUBLIC", "PRIVATE", "UNLISTED"}
    return value if value in allowed else "PRIVATE"

def sanitize_title(title):
    if not title:
        return "Untitled Playlist"
    
    for char in ["<", ">"]: # ytmusic will crash if these are part of the title
        title = title.replace(char, "")
    
    if not title.strip():
        return "Untitled Playlist"
    
    return title.strip()

def main():
    logger.info("Starting YouTube Music migration...")

    try:
        spotify_data = load_spotify_data()
        if not spotify_data:
            logger.warning("No playlists found in Spotify data")
            sys.exit(0)

        if not isinstance(spotify_data, dict):
            logger.error("Spotify data format invalid (expected dict)")
            sys.exit(1)
    except Exception as e:
        logger.exception("Failed to load Spotify data")
        sys.exit(1)

    ytmusic = ensure_ytmusic_auth()
    created_playlists = {}
    failed_playlists = []

    for _, playlist_info in spotify_data.items():
        playlist_id = None

        details = playlist_info.get("details", {})

        if details.get("User Created") != "True":
            continue

        title = sanitize_title(details.get("Name", "Untitled Playlist"))
        description = details.get("Description", "")
        privacy = map_privacy(details.get("Discoverability", "PRIVATE"))

        logger.info(f"\nProcessing playlist: {title}")

        tracks = playlist_info.get("tracks", [])
        video_ids, number_of_tracks = get_video_ids(ytmusic, tracks)

        logger.info("-" * 50)
        logger.info("Creating playlist: %s", title)

        if not video_ids:
            logger.info("No tracks resolved. Skipping playlist.")
            continue
        
        max_retries = 1 # no retries as of now because of rate limiting
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                resp = ytmusic.create_playlist(
                    title=title,
                    description=description,
                    privacy_status=privacy
                )

                if isinstance(resp, dict):
                    playlist_id = resp.get("playlistId") or resp.get("browseId")
                else:
                    playlist_id = resp

                if not isinstance(playlist_id, str) or not playlist_id:
                    logger.warning("Invalid response from YouTube Music API: %r", resp)
                    
                    if isinstance(resp, dict) and "actions" in resp:
                        logger.warning("YouTube Music may be rate-limiting. Waiting 30 seconds...")
                        time.sleep(30)
                        retry_count += 1
                        continue
                    else:
                        raise ValueError("Invalid playlist ID returned")
                
                logger.info(f"Empty Playlist created: https://music.youtube.com/playlist?list={playlist_id}")
                break

            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    logger.exception("Failed to create playlist after %d attempt(s)", max_retries)
                    failed_playlists.append(title)
                    break
                else:
                    logger.warning("Retry %d/%d after error: %s", retry_count, max_retries, str(e))
                    time.sleep(10 * retry_count)  # Exponential backoff

        if not playlist_id:
            continue
        
        created_playlists[title] = playlist_id
        logger.info("Songs will be added in batches of 50.")

        try:
            logger.info(f"Adding songs to playlist: {title}. https://music.youtube.com/playlist?list={playlist_id}")
            batch_cnt = 1
            
            for i in range(0, number_of_tracks, 50):
                batch = video_ids[i : i + 50]

                if not batch:
                    break

                logger.info(f"Adding batch {batch_cnt} ({len(batch)} songs)")
                batch_cnt += 1

                try:
                    ytmusic.add_playlist_items(
                        playlistId=playlist_id,
                        videoIds=batch,
                        duplicates=True
                    )
                    logger.info(f"Successfully added batch {batch_cnt - 1}")

                except Exception:
                    logger.exception(
                        "Failed adding songs %d-%d to playlist %s",
                        i,
                        i + len(batch),
                        title
                    )
                    break

                time.sleep(DELAY_CONST_HIGH + random.random() * DELAY_CONST_LOW)

        except Exception:
            logger.exception(f"Could not complete addition of songs to {title}.")
        
        # WaittTTTTTTT
        logger.info(f"Waiting {PLAYLIST_CREATION_DELAY} seconds before next playlist...")
        time.sleep(
            PLAYLIST_CREATION_DELAY 
            + random.random() 
            * (DELAY_CONST_HIGH / DELAY_CONST_LOW)
        )

    logger.info("\n" + "=" * 50)
    logger.info("Migration completed.")
    logger.info("Playlists created: %d", len(created_playlists))
    
    if failed_playlists:
        logger.warning("Failed playlists (%d): %s", len(failed_playlists), ", ".join(failed_playlists))
    
    logger.info("Log file saved to: %s", LOG_FILE.resolve())

if __name__ == "__main__":
    main()
