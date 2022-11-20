import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Handling time and unix timestamp
import time
import datetime
import dateutil.parser

# Load env variables
from dotenv import dotenv_values

def fetch_data():

    config = dotenv_values(".env")

    scope = "user-read-recently-played"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth( client_id=config.get("SPOTIPY_CLIENT_ID"),
                                                    client_secret=config.get("SPOTIPY_CLIENT_SECRET"),
                                                    redirect_uri=config.get("SPOTIPY_REDIRECT_URI"),
                                                    scope=scope))

    # Fetch last 50 played songs
    results = sp.current_user_recently_played(limit=50)

    # Last saved timestamp
    f = open("last-stamp.save", "r")
    stamp = f.read()

    # Save new data in seperate string
    newData = ''

    for idx, item in enumerate(results['items']):

        # only take songs, older then last timestamp
        if  int(dateutil.parser.parse(item["played_at"]).strftime('%s')) > int(stamp):

            track = item['track']
            newData = newData + track['artists'][0]['name'] + " - " + track['name'] + "\n"

        # At index zero, the last 
        if idx == 0:
            last_stamp = item["played_at"]

    # Write new data at beginning of existing file
    with open('history.txt', 'r') as original: data = original.read()
    original.close()
    with open('history.txt', 'w') as modified: modified.write(newData + data)
    modified.close()

    # Save last time stamp from data
    # Format out of api:
    # 2022-11-18T23:09:04.344Z
    d = dateutil.parser.parse(last_stamp).strftime('%s')
    f = open("last-stamp.save", "w")
    f.write(str(d))
    f.close()

if __name__ == '__main__':

    # If somethign went wrong, write into new logfile
    try:
        fetch_data()
    except e:
        f = open('logs/' + str(datetime.now().strftime("%H:%M:%S")) +  "_error.log", "w") 
        f.write(e)
        f.close()



