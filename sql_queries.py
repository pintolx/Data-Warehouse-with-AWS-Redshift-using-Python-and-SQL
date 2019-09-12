import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# This table logs all items in the log_data json files from the S3 bucket
staging_events_table_create= ("""CREATE TABLE IF NOT EXISTS staging_events(
    event_id INT IDENTITY(0,1),
    artist_name VARCHAR(255),
    auth VARCHAR(50),
    user_first_name VARCHAR(255),
    user_gender  VARCHAR(1),
    item_in_session	INTEGER,
    user_last_name VARCHAR(255),
    song_length	DOUBLE PRECISION, 
    user_level VARCHAR(50),
    location VARCHAR(255),	
    method VARCHAR(25),
    page VARCHAR(35),	
    registration VARCHAR(50),	
    session_id	BIGINT,
    song_title VARCHAR(255),
    status INTEGER,
    ts VARCHAR(50),
    user_agent TEXT,	
    user_id VARCHAR(100));
""") 

# This table logs all items in the song_data json files from the S3 bucket
staging_songs_table_create = ("""CREATE TABLE IF NOT EXISTS staging_songs(
    song_id VARCHAR(100),
    num_songs INTEGER,
    artist_id VARCHAR(100),
    artist_latitude DOUBLE PRECISION,
    artist_longitude DOUBLE PRECISION,
    artist_location VARCHAR(255),
    artist_name VARCHAR(255),
    title VARCHAR(255),
    duration DOUBLE PRECISION,
    year INTEGER);
""")
#Logs log data associated with song plays for all records with page = NextSong

#This table logs all the information about users in the app
user_table_create = (""" CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    gender VARCHAR(1),
    level VARCHAR(50));
""")
#Stores decriptive information about the songs
song_table_create = (""" CREATE TABLE IF NOT EXISTS songs (
    song_id VARCHAR(100),
    title VARCHAR(255),
    artist_id VARCHAR(100) NOT NULL,
    year INTEGER,
    duration DOUBLE PRECISION);
""")
#This table stores all the information about the artists in the music database
artist_table_create = (""" CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR(100),
    name VARCHAR(255),
    location VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION);
""")
#This table logs time stamps of all the music thats played from the songplays table and it breaks it down to specific units
time_table_create = (""" CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday INTEGER);
""")
songplay_table_create = ("""CREATE TABLE IF NOT EXISTS songplays (
    songplay_id INT IDENTITY(0,1),
    start_time TIMESTAMP,
    user_id VARCHAR(50),
    level VARCHAR(50),
    song_id VARCHAR(100),
    artist_id VARCHAR(100),
    session_id BIGINT,
    location VARCHAR(255),
    user_agent TEXT);
""")

# STAGING TABLES

staging_events_copy = ("""copy staging_events from '{}'
 credentials 'aws_iam_role={}'
 region 'us-west-2' 
 COMPUPDATE OFF STATUPDATE OFF
 JSON '{}'""").format(config.get('S3','LOG_DATA'), config.get('IAM_ROLE', 'ARN'), config.get('S3','LOG_JSONPATH'))

staging_songs_copy = ("""copy staging_songs from '{}'
    credentials 'aws_iam_role={}'
    region 'us-west-2' 
    COMPUPDATE OFF STATUPDATE OFF
    JSON 'auto' """).format(config.get('S3','SONG_DATA'), config.get('IAM_ROLE', 'ARN'))

# FINAL TABLES
songplay_table_insert = ("""INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent) 
    SELECT DISTINCT TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time, r.user_id, r.user_level, f.song_id, f.artist_id, r.session_id, r.location, r.user_agent
    FROM staging_events r, staging_songs f
    WHERE r.page = 'NextSong'
    AND r.song_title = f.title
    AND user_id NOT IN (SELECT DISTINCT p.user_id FROM songplays p WHERE p.user_id = user_id
                       AND p.start_time = start_time AND p.session_id = session_id )
""")

user_table_insert = ("""INSERT INTO users (user_id, first_name, last_name, gender, level)  
    SELECT DISTINCT user_id, user_first_name, user_last_name, user_gender, user_level
    FROM staging_events
    WHERE page = 'NextSong'
    AND user_id NOT IN (SELECT DISTINCT user_id FROM users)
""")

song_table_insert = ("""INSERT INTO songs (song_id, title, artist_id, year, duration) 
    SELECT DISTINCT song_id, title, artist_id, year, duration
    FROM staging_songs
    WHERE song_id NOT IN (SELECT DISTINCT song_id FROM songs)
""")

artist_table_insert = ("""INSERT INTO artists (artist_id, name, location, latitude, longitude) 
    SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
    FROM staging_songs
    WHERE artist_id NOT IN (SELECT DISTINCT artist_id FROM artists)
""")

time_table_insert = ("""INSERT INTO time (start_time, hour, day, week, month, year, weekday)
    SELECT start_time, EXTRACT(hr from start_time) AS hour, EXTRACT(d from start_time) AS day, EXTRACT(w from start_time) AS week, EXTRACT(mon from start_time) AS month, EXTRACT(yr from start_time) AS year, EXTRACT(weekday from start_time) AS weekday 
    FROM (
    	SELECT DISTINCT  TIMESTAMP 'epoch' + ts/1000 *INTERVAL '1 second' as start_time 
        FROM staging_events s )
    WHERE start_time NOT IN (SELECT DISTINCT start_time FROM time)
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]