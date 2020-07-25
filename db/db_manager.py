import logging
import os
import sys

from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(__name__)

if "MONGODB_URI" not in os.environ:
    logger.fatal("MONGODB_URI not provided")
    sys.exit(0)

MONGODB_URI = os.environ.get("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.get_default_database()


def save_new(station, now_playing_json):
    artist = str(now_playing_json["artist"])
    title = str(now_playing_json["title"])
    logger.info("[" + station + "] - " + "Saving: " + artist + " - " + title)
    try:
        collection = db[station + "_nowplaying"]
        db_result = collection.insert_one(now_playing_json)
        logger.info("[" + station + "] - " + "Saved to nowplaying. _id: " + str(db_result.inserted_id) +
                    " acknowledged: " + str(db_result.acknowledged))
        save_in_songs(station, now_playing_json)
    except DuplicateKeyError:
        logger.fatal("Duplicate Key Error. This should never happen, and is last resort data check from the db.")


def save_in_songs(station, songdata):
    query = {"artist": str(songdata["artist"]), "title": str(songdata["title"])}
    update = {"$set": {"last_heard": songdata["start_time"], "spotify": songdata["spotify"]},
              "$inc": {"num_plays": 1},
              "$setOnInsert": {"artist": songdata["artist"], "title": songdata["title"],
                               "first_heard": songdata["start_time"]}}
    collection = db[station + "_songs"]
    db_result = collection.update_one(query, update, upsert=True)
    logger.info("[" + station + "] - " + "Saved to songs. Matched Count: " + str(db_result.matched_count) +
                " Modified Count: " + str(db_result.modified_count) + " UpsertedID: " + str(db_result.upserted_id))


def get_last_streamed(station):
    collection = db[station + "_nowplaying"]
    last = collection.find({}).sort("start_time", direction=DESCENDING).limit(1).next()
    return last


def check_init_db(station):
    logger.info("[" + station + "] - " + "Checking Database")
    if str(station) + "_nowplaying" in db.collection_names():
        stats = db.command("collstats", str(station) + "_nowplaying")
        if stats["count"] == 0:
            insert_nowplaying_dummy(station)
    else:
        logger.info("[" + station + "] - " + "Must be the first run. Creating Collections")
        db.create_collection(name=str(station + "_nowplaying"))
        db.create_collection(name=str(station + "_songs"))
        insert_nowplaying_dummy(station)
    # Indices
    logger.info("[" + station + "] - " + "Checking Indices")
    db[str(station + "_nowplaying")].create_index([("start_time", DESCENDING)], unique=True, background=True)
    db[str(station + "_songs")].create_index([("artist", ASCENDING)], background=True)
    db[str(station + "_songs")].create_index([("title", ASCENDING)], background=True)


def insert_nowplaying_dummy(station):
    # Insert dummy record
    data = dict()
    data["artist"] = "Some Artist"
    data["title"] = "Some Title"
    data["album_title"] = "Album Title"
    collection = db[station + "_nowplaying"]
    collection.insert_one(data)
