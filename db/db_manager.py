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
    logging.info('Saving: ' + songdata['artist']['name'] + " - " + songdata['song']['name'])
    db.nowplaying.insert_one(songdata)


def get_last_streamed():
    last = db.nowplaying.find({}).sort("_id", direction=DESCENDING).limit(1).next()
    return last


def check_init_db():
    if 'nowplaying' in db.collection_names():
        stats = db.command("collstats", "nowplaying")
        if stats['count'] == 0:
            insert_nowplaying_dummy()
    else:
        insert_nowplaying_dummy()


def insert_nowplaying_dummy():
    # Insert dummy record
    data = {'artist': {}, 'song': {}}
    data['artist']['id'] = ''
    data['artist']['name'] = 'Some Artist'
    data['song']['id'] = ''
    data['song']['name'] = 'Some Song Name'
    data['song']['albumName'] = 'Some Album Name'
    data['startTime'] = '2016-06-29T16:06:23.016Z'
    db.nowplaying.insert_one(data)