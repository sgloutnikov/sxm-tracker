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

station = 'theheat'
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()
collection_nowplaying = db[station + '_nowplaying']
collection_songs = db[station + '_songs']

scrub_manager.init(station)

#songs = db.nowplaying.find({'song': {"$regex": 'Break Up'}}).sort("startTime", direction=ASCENDING)
songs = collection_nowplaying.find({"song": "P.I.M.P.", "spotify.url": ""}).sort("startTime", direction=ASCENDING)

counter = 1
for song in songs:

    print(str(counter))
    print(song)
    song_id = song.get('_id')
    song = scrub_manager.scrub_artist(station, song)
    print(song)
    song = scrub_manager.scrub_song(station, song)
    print(song)
    song = api_manager.get_spotify(song)
    song.pop('_id', None)
    print(song)
    collection_nowplaying.replace_one({'_id': ObjectId(song_id)}, song)
    db_manager.save_in_songs(station, song)
    counter += 1
    time.sleep(0.5)
