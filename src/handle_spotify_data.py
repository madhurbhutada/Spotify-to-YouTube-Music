import requests as HTTPReq

def getPlaylistTracks(details, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    epBase = details.get('tracks', {}).get('href', '')

    if not epBase:
        return []
        
    limit = 50
    offset = 0
    tracks = []

    while True:
        params = {
            'limit' : limit,
            'offset' : offset
        }

        response = HTTPReq.get(
            epBase, headers=headers, params=params)
        # import json
        # with open('tracks.json', 'w', encoding='utf-8') as f:
        #     json.dump(tracks, f, ensure_ascii=False, indent=4)

        if response.status_code != 200:
            print(f"Error {response.status_code} - {response.text}")
            break

        response_data = response.json()

        items = response_data.get('items', [])
        if not items:
            break

        for item in items:
            track = item.get('track')
            
            if not track:
                continue

            artists = [
                artist.get('name', '') for artist in track.get('artists', [])
                if artist.get('name')
            ]

            if not track.get('name') and not artists:
                continue

            tracks.append({
                'name': track.get('name', ''),
                'artists': ", ".join(artists) if artists else ''
            })

        offset += limit
        if offset >= response_data.get('total', 0):
            break

    return tracks

def handle_data(playlists, access_token, user_id):
    user_display_data = []
    user_migration_data = {}

    for details in playlists['items']:
        user_created = 'True' if details.get('owner', {}).get('id') == user_id else 'False'
        if not user_created:
            continue
        
        playlist_id = details['id']

        user_display = {
            'id': playlist_id,
            'Name': details.get('name', 'No Name'),
            'Description': details.get('description', ''),
            'Discoverability': 'PUBLIC' if details.get('public') else 'PRIVATE',
            'Collaborative': details.get('collaborative', False),
            'Number of songs': details.get('tracks', {}).get('total', 0),  # default to 0 if tracks are missing
            'User Created': user_created
        }

        user_display_data.append(user_display)

        user_migration_data[playlist_id] = {
            'details' : user_display,
            'tracks': getPlaylistTracks(details, access_token)
        }

    return user_display_data, user_migration_data
