import logging
import os
import re
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
    logging.info('++ Saving: ' + artist + " - " + song)
    db_result = db.nowplaying.insert_one(songdata)
    logging.info('Saved _id: ' + str(db_result.inserted_id) + " acknowledged: " + str(db_result.acknowledged))

def get_last_streamed():
    last = db.nowplaying.find({}).sort("_id", direction=DESCENDING).limit(1).next()
    return last


#TODO: Load in memory... Original thought was to be able to change filters in live app without restarting.
def is_clean(artist, song):
    # Artist Check
    with open('tools/filter_lists/bad_artist.txt', 'r') as f:
        for line in f:
            pattrn = str(line).strip()
            REGEX = re.compile(pattrn, re.IGNORECASE)
            if REGEX.search(artist):
                logging.info("Dirty Artist Filter Matched! " + artist + " - " + song + " -> " + pattrn)
                return False
    # Song Check
    with open('tools/filter_lists/bad_song.txt', 'r') as f:
        for line in f:
            pattrn = str(line).strip()
            REGEX = re.compile(pattrn, re.IGNORECASE)
            if REGEX.search(song):
                logging.info("Dirty Song Filter Matched! " + artist + " - " + song + " -> " + pattrn)
                return False
    # Passed Filters
    return True


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
    data['spotify'] = {}
    data['spotify']['artist'] = ''
    data['spotify']['song'] = ''
    data['spotify']['url'] = ''
    data['spotify']['uri'] = ''
    data['spotify']['album'] = ''
    data['spotify']['album_image'] = ''
    db.nowplaying.insert_one(data)