# Clean bad data from db based on pre-configured strings.

from ..db import db_manager
import re
import os

total = 0
print("--- Starting Manual DB Clean ---")

# Artist
print("--- Artist ---")
fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/bad_artist.txt')
with open(fpath, 'r') as f:
    for line in f:
        pattrn = str(line).strip()
        print("Checking: " + pattrn)
        REGEX = re.compile(pattrn, re.IGNORECASE)
        # Remove Here
        result = db_manager.db.nowplaying.delete_many(({'artist': {'$regex': REGEX}}))
        total += result.deleted_count
        print("Deleted: " + str(result.deleted_count))


# Song
print("--- Song ---")
fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/bad_song.txt')
with open(fpath, 'r') as f:
    for line in f:
        pattrn = str(line).strip()
        print("Checking: " + pattrn)
        REGEX = re.compile(pattrn, re.IGNORECASE)
        # Remove Here
        result = db_manager.db.nowplaying.delete_many(({'song': {'$regex': REGEX}}))
        total += result.deleted_count
        print("Deleted: " + str(result.deleted_count))


print("--- Finished Manual DB Clean ---")
print("Total Records Deleted: " + str(total))
