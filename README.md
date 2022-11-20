# Spotify Listening Database
Save user listening data in database for keeping precise history.

## Running the script

1. Create Spotify Dashboard in developer page

2. Fill the data in the .env for authorize your Spotify. 

3. Add this to crontab -e

In X you can fill your time between execution.

```
*/X * * * * /home/<path-to-your-repo>/spotify-listening-database/src/scripts/fetch-data.py
```

Then every X Minutes the script save all recent data without dublicates.