import spotipy
import requests
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread

SPOTIPY_CLIENT_ID = #"YOUR CLIENT ID"
SPOTIPY_CLIENT_SECRET= #"YOUR CLIENT SECRET"
SPOTIPY_REDIRECT_URL="http://127.0.0.1:9090"
SCOPE="user-top-read"

#Authentication
sp=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                             client_secret=SPOTIPY_CLIENT_SECRET,
                                             redirect_uri=SPOTIPY_REDIRECT_URL,
                                             scope=SCOPE))


#Get user's top track
def get_tracks_id(time_frame):
    track_ids=[]
    for song in time_frame['items']:
        track_ids.append(song['id'])
    return track_ids

#Get track's feature such as artist's name, albumn, track's image and URL
def get_track_features(id):
    meta=sp.track(id)
    name=meta['name']
    album=meta['album']['name']
    artist=meta['album']['artists'][0]['name']
    spotify_url=meta['external_urls']['spotify']
    album_cover=meta['album']['images'][0]['url']
    track_info=[name, album, artist, spotify_url, album_cover]

    return track_info

#Insert all the track's data into a google sheet
def insert_to_gsheet(track_ids):
 
    tracks = []
    for i in range(len(track_ids)):
        time.sleep(.5)
        track = get_track_features(track_ids[i])
        tracks.append(track)

    df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'spotify_url', 'album_cover'])

    gc = gspread.service_account(filename='spotify-wrapped-408406-9eda9ff82713.json')
    sh = gc.open(#'YOUR GOOGLE SHEET NAME')
    worksheet = sh.worksheet(f'{time_period}')
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())
    print('Done')

#Get 20 tracks from 3 time period ranging from recent most listened track to all time most listened tracks
time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_tracks_id(top_tracks)
    insert_to_gsheet(track_ids)


