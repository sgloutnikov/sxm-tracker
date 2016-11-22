import logging
import os
import re
from itertools import filterfalse

logger = logging.getLogger(__name__)


# Run through replace definitions, and replace matches. Allow for live definitions changes.
def replace_definitions(song_json):
    artist = str(song_json['artist'])
    logger.info("Artist Before Replace Scrub: " + artist)
    fpath = os.path.join(os.path.dirname(__file__), '../filter_lists/edit_replace_artist.txt')
    with open(fpath, 'r') as f:
        for line in filterfalse(__is_comment, f):
            line_list = str(line).rsplit(',', 1)
            search = line_list[0]
            replace = line_list[1].strip()
            search_pattern = re.compile(search)
            if re.search(search_pattern, artist):
                artist_repl = re.sub(search_pattern, replace, artist)
                song_json['artist'] = artist_repl
                logger.info("Artist After Replace Scrub: " + artist_repl)
    return song_json


def __is_comment(s):
    return s.startswith('#')
