import pandas as pd
import sys, os

################################################
############   Write into file    ##############
write_into_file = True
################################################


def print_df(content):
    print(content)
    print('############################################################')


def most_listen_artist(df, limit=20):
    print_df(df['master_metadata_album_artist_name'].value_counts().head(limit))


def most_listen_track(df, limit=20):
    print_df(df[['master_metadata_track_name', 'master_metadata_album_artist_name']].value_counts().head(limit))


def most_listen_album(df, limit=20):
    print_df(df[['master_metadata_album_album_name', 'master_metadata_album_artist_name']].value_counts().head(limit))


def get_first_song(df, limit=20):
    df = df.sort_values(by='ts', ascending=True)
    print(df[['ts', 'master_metadata_track_name', 'master_metadata_album_artist_name']].head(limit))


def most_listen_in_coutry(df, limit=20):
    print_df(df['conn_country'].value_counts().head(limit))


def get_albums_for_artist(df, artist, limit=20):
    df =  df.query('master_metadata_album_artist_name == "%s"' % artist)
    print('#################### Songs for Artist: %s ####################' % artist )
    most_listen_album(df)


def get_songs_for_artist(df, artist, limit=20):
    df =  df.query('master_metadata_album_artist_name == "%s"' % artist)
    print('#################### Songs for Artist: %s ####################' % artist )
    most_listen_track(df)


def minutes_played_overall(df):
    print( 'Hours played: %s \nThats %s days!' \
        % ( (df['ms_played'].sum() / 3600000).round(2), \
            (df['ms_played'].sum() / 3600000 / 24).round(2)))


def most_listen_in_year(df, year):
    df =  df.query('"%s" > ts > "%s"' % (year+1, year-1))
    print('Most listen in year %s' % year)
    count_minutes(df)


def most_listen_song_in_year(df, year):
    filter = '"%s" > ts > "%s"' % (year+1, year-1)
    df =  df.query(filter)
    print('Most listen tracks in year %s' % year)
    most_listen_track(df)


def count_minutes(df):
    limit=20
    df2= df.groupby('master_metadata_album_artist_name')['ms_played'] \
                            .sum() \
                            .sort_values(ascending=False) \
                            .reset_index(name ='ms_played') \
                            .head(limit)

    df2['h_played'] = (df2['ms_played'] / 3600000).round(2)

    print_df(df2)


def load_data():
    directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'ext')
    filename = 'full_history.csv'


    df = pd.read_csv(os.path.join(directory, filename))

    df= df[df['ms_played'] != 0]

    df['ts'] = pd.to_datetime(df.ts)
    df['ts'] = pd.to_datetime(df["ts"].dt.strftime('%Y'))

    return df 


def analyze():
    df = load_data()

    print_df(df.info())

    most_listen_artist(df)
    most_listen_track(df)
    most_listen_album(df)
    
    most_listen_in_coutry(df)

    count_minutes(df)

    get_albums_for_artist(df, 'Kraftklub')
    get_songs_for_artist(df, 'Kraftklub')

    most_listen_in_coutry(df)

    get_first_song(df, 10)

    for year in range(2014, 2023):
        most_listen_in_year(df, year)
        most_listen_song_in_year(df, year)
        print('############################################################')
        print('############################################################')

    minutes_played_overall(df)

if __name__ == '__main__':

    if write_into_file:
        sys.stdout = open("summary.txt", "w")
        analyze()
        sys.stdout.close()
    else:
        analyze()
