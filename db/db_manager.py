import os
import logging.config
from pymongo import MongoClient

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)

MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()
logger.info("DB Initialized.")


def save_full_sample_data(data):
    db.sampledata.insert_one(data)


# TODO: getLastStreamed, saveNewSong




