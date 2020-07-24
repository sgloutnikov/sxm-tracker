import logging
import re
from itertools import filterfalse
import os
from . import artist_scrub
from . import song_scrub

logger = logging.getLogger(__name__)

bad_artists = dict()
bad_titles = dict()


def scrub_artist(station, now_playing_json):
    now_playing_json = artist_scrub.replace_definitions(station, now_playing_json)
    return now_playing_json


def scrub_title(station, now_playing_json):
    now_playing_json = song_scrub.strip_year_tag(now_playing_json)
    now_playing_json = song_scrub.replace_definitions(station, now_playing_json)
    return now_playing_json


def is_clean(station, artist, title):
    # Artist Check
    for artist_filter in bad_artists[station]:
        REGEX = re.compile(artist_filter, re.IGNORECASE)
        if REGEX.search(str(artist)):
            logger.info("Dirty Artist Filter Matched! " + artist + " - " + title + " -> " + artist_filter)
            return False
    # Song Check
    for song_filter in bad_titles[station]:
        REGEX = re.compile(song_filter, re.IGNORECASE)
        if REGEX.search(str(title)):
            logger.info("Dirty Song Filter Matched! " + artist + " - " + title + " -> " + song_filter)
            return False
    # Passed Filters
    return True


def __is_comment(s):
    return s.startswith("#")


def init(station):
    logger.info("[" + station + "] - " + "Loading Bad Filter Lists")
    # Load Bad Artists List
    bad_artists_list = []
    fpath = os.path.join(os.path.dirname(__file__), "../filter_lists/" + station + "/bad_artist.txt")
    with open(fpath, "r") as f:
        for line in filterfalse(__is_comment, f):
            bad_artists_list.append(str(line).strip())
    bad_artists[station] = bad_artists_list
    # Load Bad Songs List
    bad_songs_list = []
    fpath = os.path.join(os.path.dirname(__file__), "../filter_lists/" + station + "/bad_song.txt")
    with open(fpath, "r") as f:
        for line in filterfalse(__is_comment, f):
            bad_songs_list.append(str(line).strip())
    bad_titles[station] = bad_songs_list
    # Init Worker Classes
    artist_scrub.init(station)
    song_scrub.init(station)

