import pandas as pd

import os

def most_listen_artist(df, limit=20):
    print(df['master_metadata_album_artist_name'].value_counts().head(limit))
    print('############################################################')


def most_listen_track(df, limit=20):
    print(df['master_metadata_track_name'].value_counts().head(limit))
    print('############################################################')


def most_listen_album(df, limit=20):
    print(df['master_metadata_album_album_name'].value_counts().head(limit))
    print('############################################################')


def most_listen_in_coutry(df, limit=20):
    print(df['conn_country'].value_counts().head(limit))
    print('############################################################')


def load_data():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ext')
    filename = 'full_history.csv'

    return pd.read_csv(os.path.join(directory, filename))


def analyze():
    df = load_data()

    df= df[df['ms_played'] != 0]

    print(df.info())

    most_listen_artist(df)
    most_listen_track(df)
    most_listen_album(df)
    most_listen_in_coutry(df)


if __name__ == '__main__':
    analyze()