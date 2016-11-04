import logging
from datetime import datetime, timedelta
import requests
import spotipy
import re

logger = logging.getLogger(__name__)

baseurl = 'https://www.siriusxm.com/metadata/pdt/en-us/json/channels/hotjamz/timestamp/'


def get_now_playing_data():
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
    return data


def get_spotify(song_json):
    spotify_api = spotipy.Spotify()

    # Check if multiple artists, if more than 2 use first 2 to prevent trimmed artist names in search
    artist_list = song_json['artist'].split('/')
    if len(artist_list) > 2:
        srch_artist = artist_list[0] + " " + artist_list[1]
    else:
        srch_artist = song_json['artist']
    # Clean search string. Remove (xx) year tags.
    srch_song = song_json['song']
    srch_song = re.sub(r'\s\(\d\d\)', '', srch_song)

    # Search Spotify
    results = spotify_api.search(q='artist:' + srch_artist + ' track:' + srch_song, limit=1, type='track')
    # If found add it
    if results['tracks']['total'] > 0:
        logging.info("Adding Spotify: " + song_json['artist'] + " - " + song_json['song'])
        spotify_track = results['tracks']['items'][0]
        song_json['spotify'] = {}

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
        song_json['spotify']['album_image'] = spotify_track['album']['images'][0]['url']

        return song_json
    else:
        logging.info("No Spotify Found: " + srch_artist + "(" + song_json['artist'] + ") - " +
                     srch_song + "(" + song_json['song'] + ")")
        return song_json
