# Manually scrub/re-scrub old entries and update them in the db.

from api import api_manager
from db import db_manager
from scrubber import scrub_manager
from pymongo import MongoClient
from pymongo import ASCENDING
from bson.objectid import ObjectId
import os
import logging
import time

logging.basicConfig(filename='db_backfil_scrub.log',level=logging.DEBUG)

MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

scrub_manager.init()

#songs = db.nowplaying.find({'song': {"$regex": 'Break Up'}}).sort("startTime", direction=ASCENDING)
songs = db.nowplaying.find({"song": "It Won't Stop"}).sort("startTime", direction=ASCENDING)

counter = 1
for song in songs:

    print(str(counter))
    print(song)
    song_id = song.get('_id')
    song = scrub_manager.scrub_artist(song)
    print(song)
    song = scrub_manager.scrub_song(song)
    print(song)
    song = api_manager.get_spotify(song)
    song.pop('_id', None)
    print(song)
    db.nowplaying.replace_one({'_id': ObjectId(song_id)}, song)
    db_manager.save_in_songs(song)
    counter += 1
    time.sleep(0.5)
