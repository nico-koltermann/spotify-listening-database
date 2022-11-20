import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dotenv import dotenv_values

import time
import datetime
import dateutil.parser

config = dotenv_values(".env")

scope = "user-read-recently-played"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=config.get("SPOTIPY_CLIENT_ID"),
                                                client_secret=config.get("SPOTIPY_CLIENT_SECRET"),
                                                redirect_uri=config.get("SPOTIPY_REDIRECT_URI"),
                                                scope=scope))

results = sp.current_user_recently_played(limit=50)

f = open("last-stamp.save", "r")
stamp = f.read()

newData = ''

for idx, item in enumerate(results['items']):

    if  int(dateutil.parser.parse(item["played_at"]).strftime('%s')) > int(stamp):

        track = item['track']

        newData = newData + track['artists'][0]['name'] + " - " + track['name'] + "\n"

    if idx == 0:
        last_stamp = item["played_at"]

with open('history.txt', 'r') as original: data = original.read()
original.close()
with open('history.txt', 'w') as modified: modified.write(newData + data)
modified.close()

# 2022-11-18T23:09:04.344Z
d = dateutil.parser.parse(last_stamp).strftime('%s')
f = open("last-stamp.save", "w")
f.write(str(d))
f.close()


