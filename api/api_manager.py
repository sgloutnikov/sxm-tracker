import logging
from datetime import datetime, timedelta
import requests
import requests.exceptions
import spotipy
import re
import time

logger = logging.getLogger(__name__)

spotify_api = spotipy.Spotify()


def get_now_playing_data(baseurl):
    timenow = (datetime.utcnow() - timedelta(minutes=1)).strftime('%m-%d-%H:%M:00')
    url = baseurl + timenow
    r = requests.get(url)
    jsondata = r.json()
    return jsondata


def extract_now_playing_data(full_json):
    data = {}
    data['artist_id'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['artists']['id']
    data['artist'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['artists']['name']
    data['song_id'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['id']
    data['song'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['name']
    data['album'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['album']['name']
    data['startTime'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['startTime']
    data['spotify'] = {}
    data['spotify']['artist'] = ''
    data['spotify']['song'] = ''
    data['spotify']['url'] = ''
    data['spotify']['uri'] = ''
    data['spotify']['album'] = ''
    data['spotify']['album_image'] = ''
    return data


def get_spotify(song_json):
    # TODO: Look to improve. Temp hack for how to not pull wrong spotify info for Beyonce - Sorry
    if str(song_json['album']) == 'Lemonade':
        return song_json
    # Check if multiple artists, use first to improve search results
    artist = str(song_json['artist'])
    artist_list = artist.split('/')
    if len(artist_list) > 1:
        srch_artist = artist_list[0]
    else:
        srch_artist = artist
    srch_song = song_json['song']

    # Escape some troublesome characters, but don't over-escape and miss searches
    if re.search(r'[*]', srch_song):
        srch_song = re.escape(srch_song)

    # Search Spotify (requests has been flaky in my tests, retry if failed)
    for i in range(0, 3):
        try:
            results = spotify_api.search(q='artist:' + srch_artist + ' track:' + srch_song, limit=1, type='track')
        except:
            logger.error("There was an error reaching Spotify WEB API. Retrying: " + str(i + 1))
            time.sleep(5)
            continue
        break

    # If found add it
    if results['tracks']['total'] > 0:
        logger.info("Adding Spotify: " + str(song_json['artist']) + " - " + str(song_json['song']))
        spotify_track = results['tracks']['items'][0]

        # Artist
        delim = ''
        spotify_artists = ''
        for artist in spotify_track['artists']:
            spotify_artists += delim
            spotify_artists += artist['name']
            delim = ', '
        song_json['spotify']['artist'] = spotify_artists
        # Song
        song_json['spotify']['song'] = spotify_track['name']
        # URL
        song_json['spotify']['url'] = spotify_track['external_urls']['spotify']
        # URI
        song_json['spotify']['uri'] = spotify_track['uri']
        # Album
        song_json['spotify']['album'] = spotify_track['album']['name']
        # Album Image
        if len(spotify_track['album']['images']) > 0:
            song_json['spotify']['album_image'] = spotify_track['album']['images'][0]['url']

        return song_json
    else:
        logger.info("No Spotify Found: " + srch_artist + " (" + str(song_json['artist']) + ") - " +
                     srch_song + " (" + str(song_json['song']) + ")")
        return song_json
