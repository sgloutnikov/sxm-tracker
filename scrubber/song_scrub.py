import logging
import os
import re
from itertools import filterfalse

logger = logging.getLogger(__name__)

replace_song_dict = {}


def replace_definitions(song_json):
    song = str(song_json['song'])
    for song_match, song_replace in replace_song_dict.items():
        pattern = re.compile(song_match)
        song = re.sub(pattern, str(song_replace), song).strip()
    song_json['song'] = song
    return song_json


# Strip the (xx)
def strip_year_tag(song_json):
    song = str(song_json['song'])
    song = re.sub(r'\s\(\d\d\)', '', song).strip()
    song_json['song'] = song
    return song_json


# If song length is 35 it has been stripped by the SXM API. Remove the last incomplete word.
def length_verification(song_json):
    song = str(song_json['song'])
    if len(song) == 35:
        song = song.rsplit(' ', 1)[0]
        song = song.rstrip(',')
    song_json['song'] = song
    return song_json


def __is_comment(s):
    return s.startswith('#')


def init():
    logger.info("Loading Song Replace Dictionary")
    # Load Song Replace Dictionary from File
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/edit_replace_song.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            line_list = str(line).split(',')
            replace_song_dict[str(line_list[0])] = str(line_list[1])
