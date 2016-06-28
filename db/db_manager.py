import logging
import os
from pymongo import MongoClient

logger = logging.getLogger(__name__)

MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()


def save_full_sample_data(data):
    db.sampledata.insert_one(data)


def save_new():
    logging.info("Logging")
    pass


def get_last_streamed():
    pass

