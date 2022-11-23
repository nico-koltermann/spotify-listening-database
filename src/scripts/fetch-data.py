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

def fetch_data():

    path_ws = os.path.dirname(os.path.abspath(__file__))

    config = dotenv_values(path_ws + '/.env')

    scope = 'user-read-recently-played'

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=config.get('SPOTIPY_CLIENT_ID'),
                                                    client_secret=config.get('SPOTIPY_CLIENT_SECRET'),
                                                    redirect_uri=config.get('SPOTIPY_REDIRECT_URI'),
                                                    scope=scope))

    # Fetch last 50 played songs
    results = sp.current_user_recently_played(limit=50)

    # create a database connection
    conn = dba.create_connection(path_ws + '/../database/spotify.db')
    
    stamp = dba.get_last_timestamp(conn)

    # Revert order, so last is latest
    items = results['items']
    items = items[::-1]

    print(items)
    for idx, item in enumerate(items):

        # Only take songs, older then last timestamp
        if  int(dateutil.parser.parse(item['played_at']).strftime('%s')) > int(stamp):

            track = item['track']
            
            with conn:

                track_json = json.dumps(track)

                task = ( 
                    track['artists'][0]['name'],
                    track['name'],
                    track_json,
                    str(dateutil.parser.parse(item['played_at']).strftime('%s')))

                dba.create_task(conn, task)

def fetch():

    # If something went wrong, write into new logfile
    try:
        fetch_data()
        print("Fetch worked at " + str(datetime.datetime.now().strftime('%H:%M:%S')))
    except Exception as e:
        print(e)
        path_ws = os.path.dirname(os.path.abspath(__file__))
        f = open(path_ws + '/logs/' + str(datetime.datetime.now().strftime('%H:%M:%S')) +  '_error.log', 'w') 
        f.write(str(e))
        f.close()

if __name__ == '__main__':

    fetch()
    scheduler = BlockingScheduler()
    scheduler.add_job(fetch, 'interval', minutes=20)
    scheduler.start()


