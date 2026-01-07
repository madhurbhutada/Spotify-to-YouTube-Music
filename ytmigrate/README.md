# Spotify to YouTube Music Playlist Migrator

1. No cloud
2. No servers
3. No API keys
4. Your data never leaves your device

---

## Verify your folder structure

```
  sp-ytm-migrate/
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

---

## Covered at the end:

1. What this tool does
2. Privacy & Security

---

## Windows - how to run

### Requirements (already included)

1. No system Python required
2. Python runtime
3. ytmusicapi

### Start the tool

Extract the downloaded zip file to your system:

1. Right-click on the zip file
2. Extract All...

Inside your extracted folder **Double-click on:**

```
run_windows.cmd
```

The script will:

1. Verify everything is present
2. Launch the migration automatically
3. Log everything for complete tranparency
4. You will be asked to follow few steps in order to make this work (this may be one-time)

---

### First-Time YouTube Music Login (this may be one-time)

You will be guided step-by-step. These steps are targeted towards Edge/Chrome/Brave.
Everything should be more or less similar in other browsers:

1. Browser opens **YouTube Music**
2. Ensure you are logged in
3. Open DevTools

   - `Ctrl + Shift + I`

4. Go to **Network** tab
5. Click **Library**
6. Find a request starting with `browse?`
7. Right-click → **Copy → Copy as fetch (Node.js)**
8. Paste into the terminal
9. Press:

   - **Enter**
   - **Ctrl + Z**
   - **Enter**

Authentication is now saved
You will NOT be asked again unless you decide to delete the browser.json file created in your folder structure.

---

## macOS - how to run

macOS still requires **setup**.
In your folder, inside runtime_templates > macos, go to python and site-packages.
You will find instructions regarding the setup.

runtime_templates/macos/python/README.txt → "Python 3 binary goes here"

runtime_templates/macos/site-packages/README.txt → "ytmusicapi package goes here"

Eventually, you need to make sure that the migrate.py script runs without errors :)

## What gets migrated

1. **User-created Spotify playlists only**
2. Playlist title
3. Description
4. Privacy setting
5. Songs (best match on YouTube Music)

Playlists not created by the user are skipped
Songs not found on YouTube Music are logged

---

## Rate limiting & safety

- Songs added in **batches of 50**
- Random delays between actions
- Extra delay between playlist creation
- Designed to avoid account throttling
- If it still occurs, the logs created will say so

---

## Logs & Troubleshooting

All activity is logged to:

```
migration_logs.log
```

As of now, macOS is incomplete. I am not sure if it works as expected.

Check this file if:

- A song is missing
- A playlist failed
- Migration was interrupted

---

## Re-Running the Tool

Safe to re-run, however, this tool does not record progress.
It will not skip already created playlists with the current implementation:

- Existing authentication reused
- New playlists will be created again
- Delete `browser.json` to force re-login

---

## Cleanup (Optional)

To fully reset:

```
browser.json
migration_logs.log
```

Delete both files.

---

## Contributing

If you:

- Improve macOS portability
- Add Linux support

Please consider contributing back ❤️

---

## Disclaimer

This project is:

- **Unofficial**
- **Not affiliated** with Spotify or YouTube
- Intended for **personal use only**

---

## What this tool does

1. Reads your Spotify playlists from `spotify_data.json`
2. Searches each song on YouTube Music
3. Creates matching playlists on your YouTube Music account
4. Logs everything for transparency and troubleshooting

---

## Privacy & Security

1. Authentication happens **via your own browser**
2. Cookies are stored **locally** in `browser.json`
3. **Nothing is uploaded or shared**
4. You can delete `browser.json` anytime to revoke access

---

Enjoy your music — now on YouTube Music 🎶
