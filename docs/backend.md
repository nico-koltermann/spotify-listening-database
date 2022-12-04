# Scripts

## Fetch-data

1. Create Spotify Dashboard in developer page

2. Fill the data in the .env for authorize your Spotify. 

3. Run the script on your PC or single-board computer (Raspberry Pi) for gathering the data over time.

Then every X Minutes the script save all recent data without dublicates.

## Load Spotify Data

1. You can request the listining history of the Spotify account at the official [account detail page](https://www.spotify.com/us/account/overview/). Then you get a e-mail with a history.json. __Important: Only for the normal history__ (For extended, the script should be adjusted)

2. Adjust path in the script for your data.json

3. By executing the script, it will write the old Spotify data into the database, remove podcast data and add the additional info, by request the data via Spotify api (Therefore the script need some time, if you want to avoid this, just don't use the additional data)

## DB-Actions

- Executing the script, creates a new SQLite database

- This file includes all db interactions

__Important__ This is only a local test backend, not supposed for public running, there is no security for sql injections of similar!

## Server 

1. Runs a simple Flask server backend for getting data by api call.