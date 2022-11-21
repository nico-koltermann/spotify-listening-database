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
    conn = create_connection(path_ws + '/../database/spotify.db')
    
    stamp = get_last_timestamp(conn)

    # Revert order, so last is latest
    items = results['items']
    items = items[::-1]

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

                create_task(conn, task)


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    conn = sqlite3.connect(db_file)

    return conn

def get_last_timestamp(conn):
    """ Get latest timesstamp from db
    :param db_file: database file
    :return: Connection object or None
    """

    sql = ''' SELECT MAX(history_stamp) FROM history; '''
    cur = conn.cursor()
    max_stamp = cur.execute(sql).fetchone()[0]
    return max_stamp
    
def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO history(artist, song, history_entry, history_stamp)
              VALUES(?,?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def fetch():

    # If something went wrong, write into new logfile
    try:
        fetch_data()
        print("Fetch worked at " + str(datetime.datetime.now().strftime('%H:%M:%S')))
    except Exception as e:
        path_ws = os.path.dirname(os.path.abspath(__file__))
        f = open(path_ws + '/logs/' + str(datetime.datetime.now().strftime('%H:%M:%S')) +  '_error.log', 'w') 
        f.write(str(e))
        f.close()


if __name__ == '__main__':

    scheduler = BlockingScheduler()
    scheduler.add_job(fetch, 'interval', minutes=20)
    scheduler.start()


