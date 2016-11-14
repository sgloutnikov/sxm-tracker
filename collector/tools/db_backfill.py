from ..api import api_manager
from ..db import db_manager
from pymongo import MongoClient
from pymongo import ASCENDING
import os
import time
import logging

# Edit Counter below. Aids with recovering from fatal errors and resuming.
logging.basicConfig(filename='db_backfil.log',level=logging.DEBUG)

# Backup
BACKUP_MONGODB_URI = os.environ.get('BACKUP_MONGODB_URI')
backup_client = MongoClient(BACKUP_MONGODB_URI)
backup_db = backup_client.get_default_database()

# Live
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

counter = 51000
counter_end = 51801
all_songs = backup_db.nowplaying_backup.find({}).sort("_id", direction=ASCENDING)[counter:counter_end]
for song in all_songs:
    print("Updating :" + str(counter))
    print(song)
    logging.info("Updating :" + str(counter))
    song['spotify'] = {}
    song['spotify']['artist'] = ''
    song['spotify']['song'] = ''
    song['spotify']['url'] = ''
    song['spotify']['uri'] = ''
    song['spotify']['album'] = ''
    song['spotify']['album_image'] = ''
    spotify_update = api_manager.get_spotify(song)
    print(spotify_update)
    db_result = db_manager.save_new(spotify_update)
    counter += 1
    time.sleep(1)
