import spotipy
from spotipy.oauth2 import SpotifyOAuth

from apscheduler.schedulers.blocking import BlockingScheduler

import sqlite3

import json

# Handling time and unix timestamp
import os
import time
import datetime
import dateutil.parser

import db_actions as dba

# Load env variables
from dotenv import dotenv_values

def get_details(sp, song, artist):

    # Fetch last 50 played songs
    result = sp.search(q='track:' + song + '%20' + 'artist:' + artist, type='track')

    print(result)

    if len(result['tracks']['items']) == 0:
        return None

    return result['tracks']['items'][0]

def load_data():
    path_ws = os.path.dirname(os.path.abspath(__file__))
    config = dotenv_values(path_ws + '/.env')

    dba.create_db(path_ws + "/../database/spotify-data.db")
    conn = dba.create_connection(path_ws + "/../database/spotify-data.db")

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=config.get('SPOTIPY_CLIENT_ID'),
                                                    client_secret=config.get('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri=config.get('SPOTIPY_REDIRECT_URI'),
                                                    scope=''))

    f = open(path_ws + '/../data/StreamingHistory0.json')
    hist0 = json.load(f)

    f = open(path_ws + '/../data/StreamingHistory1.json')
    hist1 = json.load(f)

    history = hist0 + hist1

    entries_count = len(history)
    print(str(entries_count) + " Entries")

    for i in range(0, len(history)):

        # TODO: get detail data
        # ret = get_details(sp, history[i]['trackName'], history[i]['artistName'])
        # print(ret['album']['artists'][0]['name'])
        # print(history[i]['trackName'])

        # podcast = ret['album']['artists']['name'] != history[i]['trackName']

        # track_json = json.dumps(ret)

        task = ( 
            history[i]['artistName'],
            history[i]['trackName'],
            # track_json,
            '',
            str(dateutil.parser.parse(history[i]['endTime']).strftime('%s')),
            history[i]['msPlayed'])

        if history[i]['msPlayed'] > 0: 
            create_task(conn, task)

        print(f'''{i} / {entries_count} Processed''')
    
def load():

    # If something went wrong, write into new logfile
    try:
        load_data()
        print("Fetch worked at " + str(datetime.datetime.now().strftime('%H:%M:%S')))
    except Exception as e:
        print(e)

if __name__ == '__main__':
    load()