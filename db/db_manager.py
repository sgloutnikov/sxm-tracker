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


def save_new(station, songdata):
    artist = str(songdata['artist'])
    song = str(songdata['song'])
    # Ensure readable timestamp
    songts = songdata['startTime']
    songdata['startTime'] = parser.parse(songts)
    logger.info("[" + station + "] - " + "Saving: " + artist + " - " + song)
    try:
        collection = db[station + '_nowplaying']
        db_result = collection.insert_one(songdata)
        logger.info("[" + station + "] - " + 'Saved to nowplaying. _id: ' + str(db_result.inserted_id) +
                    " acknowledged: " + str(db_result.acknowledged))
        save_in_songs(station, songdata)
    except DuplicateKeyError:
        logger.fatal("Duplicate Key Error. This should never happen, and is last resort data check from the db.")


def save_in_songs(station, songdata):
    query = {'artist': str(songdata['artist']), 'song': str(songdata['song'])}
    update = {'$set': {'last_heard': songdata['startTime'], 'spotify': songdata['spotify']},
              '$inc': {'num_plays': 1},
              '$setOnInsert': {'artist': songdata['artist'], 'artist_id': songdata['artist_id'],
                               'song': songdata['song'], 'song_id': songdata['song_id'],
                               'first_heard': songdata['startTime']}}
    collection = db[station + '_songs']
    db_result = collection.update_one(query, update, upsert=True)
    logger.info("[" + station + "] - " + "Saved to songs. Matched Count: " + str(db_result.matched_count) +
                " Modified Count: " + str(db_result.modified_count) + " UpsertedID: " + str(db_result.upserted_id))


def get_last_streamed(station):
    collection = db[station + '_nowplaying']
    last = collection.find({}).sort("startTime", direction=DESCENDING).limit(1).next()
    return last


def check_init_db(station):
    logger.info("[" + station + "] - " + "Checking Database")
    if str(station) + '_nowplaying' in db.collection_names():
        stats = db.command("collstats", str(station) + '_nowplaying')
        if stats['count'] == 0:
            insert_nowplaying_dummy(station)
    else:
        logger.info("[" + station + "] - " + "Must be the first run. Creating Collections")
        db.create_collection(name=str(station + '_nowplaying'))
        db.create_collection(name=str(station + '_songs'))
        insert_nowplaying_dummy(station)
    # Indices
    logger.info("[" + station + "] - " + "Checking Indices")
    db[str(station + '_nowplaying')].create_index([('startTime', DESCENDING)], unique=True, background=True)
    db[str(station + '_songs')].create_index([('artist', ASCENDING)], background=True)
    db[str(station + '_songs')].create_index([('song', ASCENDING)], background=True)


def insert_nowplaying_dummy(station):
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
    collection = db[station + '_nowplaying']
    collection.insert_one(data)
