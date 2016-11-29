# Clean bad data from db based on pre-configured strings.

from db import db_manager
import re
import os

station = 'thehighway'
collection = db_manager.db[station + "_nowplaying"]
total = 0
print("--- Starting Manual DB Clean ---")

# Artist
print("--- Artist ---")
fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/' + station + '/bad_artist.txt')
with open(fpath, 'r') as f:
    for line in f:
        pattrn = str(line).strip()
        print("Checking: " + pattrn)
        REGEX = re.compile(pattrn, re.IGNORECASE)
        # Remove Here
        result = collection.delete_many(({'artist': {'$regex': REGEX}}))
        total += result.deleted_count
        print("Deleted: " + str(result.deleted_count))


# Song
print("--- Song ---")
fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/' + station + '/bad_song.txt')
with open(fpath, 'r') as f:
    for line in f:
        pattrn = str(line).strip()
        print("Checking: " + pattrn)
        REGEX = re.compile(pattrn, re.IGNORECASE)
        # Remove Here
        result = collection.delete_many(({'song': {'$regex': REGEX}}))
        total += result.deleted_count
        print("Deleted: " + str(result.deleted_count))


print("--- Finished Manual DB Clean ---")
print("Total Records Deleted: " + str(total))
