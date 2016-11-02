import logging
import os
from pymongo import MongoClient
from pymongo import DESCENDING

logger = logging.getLogger(__name__)

MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()


def save_full_sample_data(data):
    db.sampledata.insert_one(data)


def save_new(songdata):
    artist = str(songdata['artist'])
    song = str(songdata['song'])
    song_id = str(songdata['song_id'])
    # TODO: Check if bad song from configured strings
    logging.info('Saving: ' + artist + " - " + song)
    db.nowplaying.insert_one(songdata)


def get_last_streamed():
    last = db.nowplaying.find({}).sort("_id", direction=DESCENDING).limit(1).next()
    return last


# TODO Check if song passes bad data filters
def is_clean(artist, song, song_id):
    return


def check_init_db():
    if 'nowplaying' in db.collection_names():
        stats = db.command("collstats", "nowplaying")
        if stats['count'] == 0:
            insert_nowplaying_dummy()
    else:
        insert_nowplaying_dummy()
    # TODO: Indices


def insert_nowplaying_dummy():
    # Insert dummy record
    data = {}
    data['artist_id'] = ''
    data['artist'] = 'Some Artist'
    data['song_id'] = ''
    data['song'] = 'Some Song Name'
    data['album'] = 'Some Album Name'
    data['startTime'] = '2016-06-29T16:06:23.016Z'
    db.nowplaying.insert_one(data)