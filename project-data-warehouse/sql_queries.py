import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

S3_LOG_DATA = config['S3']['LOG_DATA']
S3_LOG_JSONPATH = config['S3']['LOG_JSONPATH']
S3_SONG_DATA = config['S3']['SONG_DATA']
IAM_ROLE_ARN = config['IAM']['ROLE_ARN']
S3_REGION = config['S3']['REGION']

# DROP TABLES
staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES
staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    artist        VARCHAR,
    auth          VARCHAR,
    firstName     VARCHAR,
    gender        VARCHAR,
    itemInSession BIGINT,
    lastName      VARCHAR,
    length        FLOAT,
    level         VARCHAR,
    location      VARCHAR,
    method        VARCHAR,
    page          VARCHAR,
    registration  FLOAT,
    sessionId     BIGINT,
    song          VARCHAR,
    status        INTEGER,
    ts            BIGINT,
    userAgent     VARCHAR,
    userId        BIGINT
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
    num_songs        INTEGER,
    artist_id        VARCHAR,
    artist_latitude  FLOAT,
    artist_longitude FLOAT,
    artist_location  VARCHAR,
    artist_name      VARCHAR,
    song_id          VARCHAR,
    title            VARCHAR,
    duration         FLOAT,
    year             SMALLINT
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays (
    songplay_id BIGINT IDENTITY(0,1) PRIMARY KEY SORTKEY,
    start_time  TIMESTAMP NOT NULL,
    user_id     BIGINT NOT NULL DISTKEY,
    level       VARCHAR NOT NULL,
    song_id     VARCHAR NOT NULL,
    artist_id   VARCHAR NOT NULL,
    session_id  BIGINT NOT NULL,
    location    VARCHAR,
    user_agent  VARCHAR
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
    user_id    BIGINT PRIMARY KEY SORTKEY,
    first_name VARCHAR NOT NULL,
    last_name  VARCHAR NOT NULL,
    gender     VARCHAR,
    level      VARCHAR
) DISTSTYLE ALL;
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
    song_id   VARCHAR PRIMARY KEY SORTKEY,
    title     VARCHAR NOT NULL,
    artist_id VARCHAR NOT NULL DISTKEY,
    year      SMALLINT,
    duration  FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
    artist_id VARCHAR PRIMARY KEY SORTKEY,
    name      VARCHAR NOT NULL,
    location  VARCHAR,
    lattitude FLOAT,
    longitude FLOAT
) DISTSTYLE ALL;
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
    start_time TIMESTAMP NOT NULL PRIMARY KEY DISTKEY SORTKEY,
    hour       SMALLINT,
    day        SMALLINT,
    week       SMALLINT,
    month      SMALLINT,
    year       SMALLINT,
    weekday    VARCHAR
);
""")

# STAGING TABLES
staging_events_copy = (f"""
COPY staging_events
FROM {S3_LOG_DATA}
IAM_ROLE {IAM_ROLE_ARN}
REGION {S3_REGION}
FORMAT AS JSON {S3_LOG_JSONPATH}
TIMEFORMAT AS 'epochmillisecs';
""")

staging_songs_copy = (f"""
COPY staging_songs
FROM {S3_SONG_DATA}
IAM_ROLE {IAM_ROLE_ARN}
REGION {S3_REGION}
FORMAT AS JSON 'auto';
""")



# FINAL TABLES
songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")

time_table_insert = ("""
""")


# QUERY LISTS
drop_table_queries = [
    staging_events_table_drop,
    staging_songs_table_drop,
    songplay_table_drop,
    user_table_drop,
    song_table_drop,
    artist_table_drop,
    time_table_drop
]


create_table_queries = [
    staging_events_table_create,
    staging_songs_table_create,
    songplay_table_create,
    user_table_create,
    song_table_create,
    artist_table_create,
    time_table_create
]

copy_table_queries = [
    staging_events_copy,
    staging_songs_copy
]

insert_table_queries = [
    user_table_insert,
    time_table_insert,
    artist_table_insert,
    song_table_insert,
    songplay_table_insert
]
