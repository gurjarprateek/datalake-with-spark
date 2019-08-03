import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    Description - This function processes data in songs directory to extract data for songs and artists dimension tables
    
    Parameters:
    cur - Cursor object for running SQL queries
    filepath - location of songs directory
    """
    
    # open song file
    df = pd.read_json(filepath, lines=True)
    # insert song record
    df_song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].drop_duplicates()
    song_data =  df_song_data.values.tolist()[0]
    #print(song_data)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    df_artist = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].drop_duplicates()
    artist_data = df_artist.values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    Description - This function processes data in logs directory to extract data for time and users dimension tables, and also songplay fact table
    
    Parameters:
    cur - Cursor object for running SQL queries
    filepath - location of logs directory
    """
        
    # open log file
    df = pd.read_json(filepath, lines=True)
    
    # filter by NextSong action
    df = df[(df.page=='NextSong')]
    
    # convert timestamp column to datetime
    df['ts'] = pd.to_datetime(df['ts'])
    
    #drop duplicates
    df = df.drop_duplicates()

    # create a timestamp column to datetime
    t = pd.to_datetime(df['ts'])
    
    # insert time data records
    time_data = (t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday)
    column_labels = ('timestamp', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday')
    time_data_dict = dict(zip(column_labels, time_data))
    time_df = pd.DataFrame.from_dict(time_data_dict).drop_duplicates()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record  df['sessionId'][index].astype('str').astype('int64')
        songplay_data = (df['ts'][index], str(df['userId'][index]), df['level'][index], songid, artistid, str(df['sessionId'][index]), df['location'][index], df['userAgent'][index])
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()