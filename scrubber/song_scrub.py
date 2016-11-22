import logging
import os
import re
from itertools import filterfalse

logger = logging.getLogger(__name__)


# Run through replace definitions, and replace matches. Allow for live definitions changes.
def replace_definitions(song_json):
    song = str(song_json['song'])
    logger.info("Song Before Replace Scrub: " + song)
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/edit_replace_song.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            line_list = str(line).rsplit(',', 1)
            search = line_list[0]
            replace = line_list[1].strip()
            search_pattern = re.compile(search)
            if re.search(search_pattern, song):
                song_repl = re.sub(search_pattern, replace, song)
                song_json['song'] = song_repl
                logger.info("Song After Replace Scrub: " + song_repl)
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
