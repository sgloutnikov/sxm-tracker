import os
from datetime import timezone
from pymongo import MongoClient


TARGET_MONGODB_URI = os.environ.get("LOCAL_MONGODB_URI")
SOURCE_MONGODB_URI = os.environ.get("REMOTE_MONGODB_URI")

target_client = MongoClient(TARGET_MONGODB_URI)
target_db = target_client.get_default_database()

source_client = MongoClient(SOURCE_MONGODB_URI)
source_db = source_client.get_default_database()

print("Number of Songs: " + str(source_db["thehighway_songs"].count()))

for song_info in source_db["thehighway_songs"].find():
    new_song_info = dict()
    new_song_info["artist"] = song_info["artist"]
    new_song_info["title"] = song_info["song"]
    # Convert time to new epoch timestamp format
    new_song_info["first_heard"] = int(song_info["first_heard"].replace(tzinfo=timezone.utc).timestamp() * 1000)
    new_song_info["last_heard"] = int(song_info["last_heard"].replace(tzinfo=timezone.utc).timestamp() * 1000)
    new_song_info["num_plays"] = song_info["num_plays"]
    new_song_info["spotify"] = dict()
    new_song_info["spotify"]["artist"] = song_info["spotify"]["artist"]
    new_song_info["spotify"]["title"] = song_info["spotify"]["song"]
    new_song_info["spotify"]["url"] = song_info["spotify"]["url"]
    new_song_info["spotify"]["uri"] = song_info["spotify"]["uri"]
    new_song_info["spotify"]["album"] = song_info["spotify"]["album"]
    new_song_info["spotify"]["album_image"] = song_info["spotify"]["album_image"]
    target_db["thehighway_songs"].insert_one(new_song_info)
