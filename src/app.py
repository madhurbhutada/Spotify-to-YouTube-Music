from flask import (
    Flask, redirect, render_template, 
    request as FlskReq,session, url_for
)
from auth import (
    generate_random_string, 
    getCodeVerifier, getParams,
    getPayload
)
from urllib.parse import urlencode
import requests as HTTPReq
from datetime import timedelta
from handle_spotify_data import handle_data
import json
from zipfile import ZipFile
import os

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent # project root
YTMIGRATE_DIR = BASE_DIR / "ytmigrate"
ZIP_OUTPUT = BASE_DIR / "sp-ytm-migrate.zip"

app = Flask(__name__)
secretKey = generate_random_string(16)
app.secret_key = secretKey
app.config['SESSION_COOKIE_SECURE'] = True  # cookies are not sent over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # javaScript cannot access cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

baseUrl = "https://accounts.spotify.com/authorize"

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/authorize")
def login():
    session["code_verifier"] = getCodeVerifier()
    auth_url = f"{baseUrl}?{urlencode(getParams(session['code_verifier']))}"
    return redirect(auth_url)

@app.route("/verified")
def verified():
    session["code"] = FlskReq.args.get('code')
    print(session["code"])
    return render_template("verified.html")

@app.route("/access_token")
def access_token():
    payload = getPayload(session["code"], session["code_verifier"])
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    response = HTTPReq.post(
        "https://accounts.spotify.com/api/token", 
        data=payload, headers=headers)
    
    def storeResponseInSession():
        session["access_token"] = response_json.get('access_token')
        session["token_type"] = response_json.get('token_type')
        session["scope"] = response_json.get('scope')
        session["expires_in"] = response_json.get('expires_in')
        session["refresh_token"] = response_json.get('refresh_token')

    if response.status_code == 200:
        response_json = response.json()
        print(response_json)
        storeResponseInSession()
        return redirect(url_for('process_request'))
    else:
        print(response.status_code)
        print(response.text)
        return redirect(url_for('error'))
    
@app.route('/process_request')
def process_request():
    headers = { 'Authorization' : 'Bearer ' + session["access_token"] }
    epBase = "https://api.spotify.com/v1"

    epUsername = f"{epBase}/me"
    user_profile = HTTPReq.get(
        url=epUsername, 
        headers=headers).json()
    session["user_id"] = user_profile.get('id')

    limit = 50
    offset = 0

    complete_user_display_data = []
    complete_user_migration_data = {}
    total_playlists = 0

    while True:
        params = {
            'limit' : limit,
            'offset' : offset
        }


        epPlaylists = f"{epBase}/users/{session['user_id']}/playlists"
        response = HTTPReq.get(
            url=epPlaylists, 
            headers=headers, 
            params=params)
        playlists = response.json()
        
        total_playlists = playlists.get('total', 0)

        # print(response.status_code)
        # print(playlists.get('href'))
        # import json
        # with open('playlists.json', 'w', encoding='utf-8') as f:
        #     json.dump(playlists, f, ensure_ascii=False, indent=4)

        user_display_data, user_migration_data = handle_data(
            playlists, 
            session['access_token'],
            session['user_id'])
        
        complete_user_display_data.extend(user_display_data)
        complete_user_migration_data.update(user_migration_data)

        offset += limit
        if offset >= total_playlists:
            break
    
    # uncompressed
    with ZipFile(ZIP_OUTPUT, "w") as zipf:
        zipf.writestr(
            "spotify_data.json",
            json.dumps(
                complete_user_migration_data,
                ensure_ascii=False,
                indent=4
            )
        )

        for root, _, files in os.walk(YTMIGRATE_DIR):
            for file in files:
                full_path = Path(root) / file

                # strip ytmigrate/
                arcname = full_path.relative_to(YTMIGRATE_DIR)

                zipf.write(full_path, arcname)
    
    return render_template("process_request.html", 
                           username=user_profile.get('display_name'),
                           playlist_count=total_playlists,
                           complete_user_display_data=complete_user_display_data)

@app.route("/error")
def error():
    return render_template("error.html")

if __name__ == '__main__':
    app.run(debug=True)
