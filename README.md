# Spotify Listening Database
Save user listening data in database for keeping precise history.

Uses SQLite Database for safe data.

Transform Spotify data and write it into database.

Use a simple Flask server as sample-backend, for running it with [front-end](https://github.com/nico-koltermann/spotify-trends) foe evaluation of account listing trends.

__Problem:__

The recently-tracks are not really accurate and also don't give the same data as the normal spotify history ([Link](https://developer.spotify.com/console/get-recently-played/)).



## Changelog 03.12.2022

First idea of this repository, was a script, that fetch the data of recent history, write it into a database. Then a server 
can provide this data for a visualization at a frontend.
No further work on the backend, because of lack of information and accuracy of the recently updated, provided by the api.

Mor information [here](docs/backend.md).
## Install environment

Install via pip with requirement.txt

```bash
sudo apt install pip
pip install -r requirements.txt
```

Install via conda:

```bash
conda env create -f environment.yaml
```