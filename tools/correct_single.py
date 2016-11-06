from api import api_manager
from db import db_manager
from pymongo import MongoClient
from pymongo import ASCENDING
import os
import time
import logging

logging.basicConfig(filename='correct_single.log',level=logging.DEBUG)

original_artist = ''
original_song = ''
new_artist = ''
new_song = ''

# Backup
BACKUP_MONGODB_URI = os.environ.get('BACKUP_MONGODB_URI')
backup_client = MongoClient(BACKUP_MONGODB_URI)
backup_db = backup_client.get_default_database()

# Live
MONGODB_URI = os.environ.get('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.get_default_database()

#TODO Given artist and song in db, rename and find spotify data

