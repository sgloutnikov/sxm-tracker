import logging
import os
import re
from itertools import filterfalse

logger = logging.getLogger(__name__)

replace_artist_dict = {}


# Run through replace dictionary, and replace matches
def replace_definitions(station, song_json):
    artist = str(song_json['artist'])
    logger.info("[" + station + "] - " + "Artist Before Replace Scrub: " + artist)
    for artist_match, artist_replace in replace_artist_dict[station].items():
        pattern = re.compile(artist_match)
        if re.search(pattern, artist):
            artist = re.sub(pattern, str(artist_replace), artist)
            logger.info("[" + station + "] - " + "Artist After Replace Scrub: " + artist)
    song_json['artist'] = artist
    return song_json


def __is_comment(s):
    return s.startswith('#')


def init(station):
    # Load Artist Replace Dictionary from File
    replace_artists = {}
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/' + station + '/edit_replace_artist.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            line_list = str(line).rsplit(';', 1)
            replace_artists[str(line_list[0])] = str(line_list[1].strip())
    replace_artist_dict[station] = replace_artists
    logger.info("[" + station + "] - " + "Loaded Artist Replace Dictionary: " +
                str(len(replace_artist_dict[station])) + " definitions.")
