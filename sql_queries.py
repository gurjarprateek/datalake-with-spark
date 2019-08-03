# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS SONGPLAYS"
user_table_drop = "DROP TABLE IF EXISTS USERS"
song_table_drop = "DROP TABLE IF EXISTS SONGS"
artist_table_drop = "DROP TABLE IF EXISTS ARTISTS"
time_table_drop = "DROP TABLE IF EXISTS TIME"

# CREATE TABLES

songplay_table_create = (""" CREATE TABLE SONGPLAYS (
  songplay_id SERIAL PRIMARY KEY
, start_time TIMESTAMP
, user_id VARCHAR(255) 
, level VARCHAR(255) 
, song_id VARCHAR(255)
, artist_id VARCHAR(255)
, session_id VARCHAR(255)
, location VARCHAR(255)
, user_agent VARCHAR(255)
, FOREIGN KEY (start_time) REFERENCES TIME (start_time)
, FOREIGN KEY (user_id) REFERENCES USERS (user_id)
, FOREIGN KEY (song_id) REFERENCES SONGS (song_id)
, FOREIGN KEY (artist_id) REFERENCES ARTISTS (artist_id)
)
""")

user_table_create = (""" CREATE TABLE USERS (
  user_id VARCHAR(255) NOT NULL PRIMARY KEY
, first_name VARCHAR(255)
, last_name VARCHAR(255)
, gender VARCHAR(50)
, level VARCHAR(50)
)
""")

song_table_create = (""" CREATE TABLE SONGS (
  song_id VARCHAR(255) NOT NULL PRIMARY KEY
, title VARCHAR(255)
, artist_id VARCHAR(255)
, year INT
, duration INT
)
""")

artist_table_create = (""" CREATE TABLE ARTISTS (
  artist_id VARCHAR(255) NOT NULL PRIMARY KEY
, name VARCHAR(255)
, location VARCHAR(255)
, latitude FLOAT(8)
, longitude FLOAT(8)
)
""")

time_table_create = ("""CREATE TABLE TIME (
  start_time TIMESTAMP NOT NULL PRIMARY KEY
, hour INT NOT NULL
, day INTEGER NOT NULL
, year_week INTEGER NOT NULL
, month INTEGER NOT NULL
, year INTEGER NOT NULL
, week_day INTEGER NOT NULL
);

""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO SONGPLAYS (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO USERS (user_id, first_name, last_name, gender, level) 
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE 
SET first_name=EXCLUDED.first_name,  
last_name=EXCLUDED.last_name,
gender=EXCLUDED.gender,
level=EXCLUDED.level
""")

song_table_insert = (""" INSERT INTO SONGS (song_id, title, artist_id, year, duration) 
VALUES(%s, %s, %s, %s, %s) 
ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""INSERT INTO ARTISTS (artist_id, name, location, latitude, longitude) 
VALUES(%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = (""" INSERT INTO TIME (start_time, hour, day, year_week, month, year, week_day) 
VALUES(%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""SELECT SONGS.song_id, SONGS.artist_id from SONGS LEFT JOIN ARTISTS ON SONGS.artist_id = ARTISTS.artist_id WHERE SONGS.title = %s AND ARTISTS.name = %s AND SONGS.duration = %s""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create, artist_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]