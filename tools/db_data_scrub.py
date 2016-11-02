# Clean bad data from db based on pre-configured strings.

from db import db_manager
import re

total = 0
print("--- Starting Manual DB Clean ---")

# Artist
print("--- Artist ---")
with open('filter_lists/bad_artist.txt', 'r') as f:
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
with open('filter_lists/bad_song.txt', 'r') as f:
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
