import logging
import os
import re
from itertools import filterfalse

logger = logging.getLogger(__name__)

replace_artist_dict = {}


# Run through replace dictionary, and replace matches
def replace_definitions(song_json):
    artist = str(song_json['artist'])
    for artist_match, artist_replace in replace_artist_dict.items():
        pattern = re.compile(artist_match)
        artist = re.sub(pattern, str(artist_replace), artist).strip()
    song_json['artist'] = artist
    return song_json


def __is_comment(s):
    return s.startswith('#')


def init():
    logger.info("Loading Artist Replace Dictionary")
    # Load Artist Replace Dictionary from File
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/edit_replace_artist.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            line_list = str(line).split(',')
            replace_artist_dict[str(line_list[0])] = str(line_list[1])
