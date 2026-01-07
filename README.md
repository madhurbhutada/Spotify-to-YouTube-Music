# First of all

A huge shoutout to open-source [ytmusicapi](https://github.com/sigma67/ytmusicapi) for making this project possible.

# Link

```

```

### Please note that unfortunately, because of rate limiting, this link is not for everyone.

### To access this app, you may need to run it locally. Details have been added.

If I have not given you access you can easily follow the steps listed below to run this on your machine (free). You need **Python 3.8+** installed.
This is very smooth for Windows, but may need some additional steps for Mac.

The steps cover:

1. Spotify authentication (Flask app)
2. Spotify Developer app creation
3. Data export flow
4. How it integrates with **ytmigrate.zip**
5. Steps written for **non-technical users**, with optional technical notes

This assumes users **clone the repository and run it locally**.

---

# Spotify -> YouTube Music Migration (complete project)

This project helps you migrate your **Spotify playlists** to **YouTube Music** in two stages:

1. **Spotify Export Tool (Web App)**
   Securely logs into Spotify and generates your playlist data.
2. **ytmigrate Tool (Offline Script)**
   Uses that data to recreate playlists on YouTube Music.

- Runs fully on your machine
- No cloud storage
- No third-party servers
- You stay in control of your accounts

---

## Part 1 - Spotify export (required)

This step **fetches your Spotify playlists** and prepares them for YouTube Music.

---

### What this does

1. Logs you into Spotify using **official Spotify OAuth**
2. Fetches **all your playlists**
3. Extracts:

- Playlist name
- Description
- Privacy
- Tracks & artists
- User created or not

4. Packages everything into `spotify_data.json`
5. Automatically bundles the **ytmigrate tool** into a ZIP file

---

# How to use locally

## Step 1 - Create a Spotify Developer App (one-time)

You **must** create a Spotify app (free).

### Go to Spotify Developer Dashboard

[https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard)

### Create an App

- Click **Create App**
- App Name: Anything
- App Type: **Web API**
- Description: Anything

### Set redirect URI

In **App Settings**, add:

```
http://127.0.0.1:5000/verified
```

This must match **exactly**, or login will fail.

### Copy credentials

Save these values:

- **Client ID**
- **Client Secret**

---

## Step 2 - Configure Environment Variables

Before running the app, set these environment variables.

### Windows (PowerShell)

```
setx SPOTIFY_CLIENT_ID "paste_your_client_id_here"
setx SPOTIFY_CLIENT_SECRET "paste_your_client_secret_here"
```

### macOS / Linux (Terminal)

```
export SPOTIFY_CLIENT_ID="paste_your_client_secret_here"
export SPOTIFY_CLIENT_SECRET="paste_your_client_secret_here"
```

Restart your terminal after setting them.

---

## Step 3 - Install Python requirements

You need **Python 3.8+** installed.

Install dependencies:

```
pip install flask requests
```

This is provided in the requirements.txt file as well.

---

## Step 4 - Run the Spotify Export App

From the **spotify_export** directory:

```
python app.py
```

You will see something like:

```
Running on http://127.0.0.1:5000
```

---

## Step 5 - Login to Spotify

1. Open browser:
   [http://127.0.0.1:5000](http://127.0.0.1:5000)
2. Click **Migrate**
3. Click **Login with Spotify**
4. Approve permissions
5. Wait while playlists are processed

---

## What happens next

After processing:

- A zip file is created:

  ```
  ytmigrate.zip
  ```

- Inside the ZIP:

  ```
    ytmigrate/
    ├── spotify_data.json          # Your exported Spotify playlists (input)
    ├── migrate.py                 # Core migration logic
    ├── run_windows.cmd            # Windows launcher (double-click)
    ├── run_macos.command          # Not added
    ├── runtime_templates/
    │   ├── windows/
    │   │     ├── python/
    │   │     │    └── python.exe
    │   │     └── site-packages/
    │   │          └── ytmusicapi/
    │   └── macos/
    │         ├── python/
    │         │   └── bin/python3  # Not added
    │         │   └── README.md
    │         └── site-packages/
    │             └── ytmusicapi/  # Not added
    │             └── README.md
    ├── migration_logs.log         # Created automatically
    └── README.md
  ```

1. For windows, this ZIP is **all you need** for YouTube Music migration
2. If you're on Mac, you may need some additional steps
3. You can move the zip to another windows machine if you want

---

## Part 2 - YouTube Music migration

Extract the zip file to your desired location.
Note that on Windows, you may be given a security warning.
Don't worry, if needed, you may open it in Notepad or a text editor to verify the file.
Once you're ready, you can launch the script.

Now follow the **ytmigrate README** (already included in the ZIP).

But in short:

### Windows

```
1. Extract ytmigrate.zip
2. Double-click run_windows.cmd
3. Follow browser login steps (one-time)
```

### macOS

```
1. Extract ytmigrate.zip
2. Set up python and site-packages (one-time)
3. Make sure migrate.py runs smoothly
4. Follow browser login steps (one-time)
```

---

## Authentication details (transparency)

### Spotify

- Uses **PKCE OAuth**
- Tokens stored in memory (Flask session)
- No database
- No tracking

### YouTube Music

- Uses your browser cookies
- Stored locally in `browser.json`
- Can be deleted anytime

---

## Logs & Output

- Spotify export: browser based
- YouTube Music migration:

  ```
  ytmigrate/migration_logs.log
  ```

---

## Cleanup for re-running (if required)

To fully reset:

- Stop Flask app
- Delete:

  ```
  ytmigrate.zip
  ytmigrate/browser.json
  ytmigrate/migration_logs.log
  ```

---

## Limitations

- Spotify “Liked Songs” are **not** playlists
- Some songs may not exist on YouTube Music
- Matching is best-effort (title + artist)
- Rate limits are handled conservatively

---

## This is for

1. Understanding how it works
2. Trying to make it as simple as possible for non-technical users (step-by-step)
3. Power users who want local control
4. Privacy-conscious users

---

## Contributions Welcome

Especially for:

- macOS embedded Python runtime
- Linux support
- Authentication improvement (strict avoidance of manual swticing between HTML templates in the browser)
- UI polish
- Improved error handling
- Improved folder structuring
- Improved architecture
- Feature additions like: import specific playlist(s), import non user created playlists, etc.
- Improved song matching

---

## Disclaimer

This project is:

- **Unofficial**
- **Not affiliated** with Spotify or YouTube
- Intended for **personal use only**

---

Additional notes (can ignore). We're using PKCE autohorization for Spotify.

1. Generates a high-entropy code verifier
2. Hashes it with SHA-256
3. Encodes it using base64url (no padding) to produce the code challenge
