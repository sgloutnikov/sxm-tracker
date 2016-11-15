import os
from pymongo import MongoClient, ASCENDING
from db import db_manager


MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

counter = 0
counter_end = 1000
all_songs = db.nowplaying.find({}).sort("startTime", direction=ASCENDING)

for song in all_songs:
    db_manager.save_in_songs(song)
