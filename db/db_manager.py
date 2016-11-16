import logging
import os
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import DuplicateKeyError
from dateutil import parser

logger = logging.getLogger(__name__)

MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()


def save_full_sample_data(data):
    db.sampledata.insert_one(data)


def save_new(songdata):
    artist = str(songdata['artist'])
    song = str(songdata['song'])
    # Ensure readable timestamp
    songts = songdata['startTime']
    songdata['startTime'] = parser.parse(songts)
    logger.info('++ Saving: ' + artist + " - " + song)
    try:
        db_result = db.nowplaying.insert_one(songdata)
        logger.info('Saved to nowplaying. _id: ' + str(db_result.inserted_id) + " acknowledged: " +
                    str(db_result.acknowledged))
        save_in_songs(songdata)
    except DuplicateKeyError:
        logger.fatal("Duplicate Key Error. This should never happen, and is last resort data check from the db.")


def save_in_songs(songdata):
    query = {'artist': str(songdata['artist']), 'song': str(songdata['song'])}
    update = {'$set': {'last_heard': songdata['startTime'], 'spotify': songdata['spotify']},
              '$inc': {'num_plays': 1},
              '$setOnInsert': {'artist': songdata['artist'], 'artist_id': songdata['artist_id'],
                               'song': songdata['song'], 'song_id': songdata['song_id'],
                               'first_heard': songdata['startTime']}}
    db_result = db.songs.update_one(query, update, upsert=True)
    logger.info("Saved to songs. Matched Count: " + str(db_result.matched_count) + " Modified Count: " +
                str(db_result.modified_count) + " UpsertedID: " + str(db_result.upserted_id))



def get_last_streamed():
    last = db.nowplaying.find({}).sort("startTime", direction=DESCENDING).limit(1).next()
    return last


def check_init_db():
    logger.info("Checking Database")
    if 'nowplaying' in db.collection_names():
        stats = db.command("collstats", "nowplaying")
        if stats['count'] == 0:
            insert_nowplaying_dummy()
    else:
        logger.info("Must be the first run. Creating Collection")
        insert_nowplaying_dummy()
    # Indices
    logger.info("Checking Indices")
    db.nowplaying.create_index([('startTime', DESCENDING)], unique=True, background=True)
    db.songs.create_index([('artist', ASCENDING)], background=True)
    db.songs.create_index([('song', ASCENDING)], background=True)


def insert_nowplaying_dummy():
    # Insert dummy record
    data = {}
    data['artist_id'] = ''
    data['artist'] = 'Some Artist'
    data['song_id'] = ''
    data['song'] = 'Some Song Name'
    data['album'] = 'Some Album Name'
    data['startTime'] = '2016-06-29T16:06:23.016Z'
    data['spotify'] = {}
    data['spotify']['artist'] = ''
    data['spotify']['song'] = ''
    data['spotify']['url'] = ''
    data['spotify']['uri'] = ''
    data['spotify']['album'] = ''
    data['spotify']['album_image'] = ''
    db.nowplaying.insert_one(data)