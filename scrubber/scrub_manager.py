import logging
import re
from itertools import filterfalse
import os
from . import artist_scrub
from . import song_scrub

logger = logging.getLogger(__name__)

bad_artists = []
bad_songs = []


def scrub_artist(song_json):
    song_json = artist_scrub.replace_definitions(song_json)
    return song_json


def scrub_song(song_json):
    song_json = song_scrub.replace_definitions(song_json)
    song_json = song_scrub.strip_year_tag(song_json)
    #song_json = song_scrub.length_verification(song_json)
    return song_json


def is_clean(artist, song):
    # Artist Check
    for artist_filter in bad_artists:
        REGEX = re.compile(artist_filter, re.IGNORECASE)
        if REGEX.search(str(artist)):
            logger.info("Dirty Artist Filter Matched! " + artist + " - " + song + " -> " + artist_filter)
            return False
    # Song Check
    for song_filter in bad_songs:
        REGEX = re.compile(song_filter, re.IGNORECASE)
        if REGEX.search(str(song)):
            logger.info("Dirty Song Filter Matched! " + artist + " - " + song + " -> " + song_filter)
            return False

    # Passed Filters
    return True


def __is_comment(s):
    return s.startswith('#')


def init():
    logger.info("Loading Bad Filter Lists")
    # Load Bad Artists List
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/bad_artist.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            bad_artists.append(str(line).strip())
    # Load Bad Songs List
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/bad_song.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            bad_songs.append(str(line).strip())
