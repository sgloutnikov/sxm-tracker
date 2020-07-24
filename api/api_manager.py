import logging
import os
import sys
from datetime import datetime, timedelta
from scrubber import song_scrub
import requests
import requests.exceptions
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import time

logger = logging.getLogger(__name__)

if "SPOTIPY_CLIENT_ID" not in os.environ:
    logger.fatal("SPOTIPY_CLIENT_ID not provided")
    sys.exit(0)
if "SPOTIPY_CLIENT_SECRET" not in os.environ:
    logger.fatal("SPOTIPY_CLIENT_SECRET not provided")
    sys.exit(0)

client_credentials_manager = SpotifyClientCredentials()
spotify_api = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_now_playing_data(sxm_api_url):
    resp = requests.get(sxm_api_url)
    json_data = resp.json()
    return resp, json_data


def extract_now_playing_data(full_json):
    # Extract now playing from full JSON
    data = dict()
    station_name = next(iter(full_json["channels"]))
    data["artist"] = full_json["channels"][station_name]["content"]["artists"][0]["name"]
    data["title"] = full_json["channels"][station_name]["content"]["title"]
    data["start_time"] = full_json["channels"][station_name]["content"]["starttime"]
    data["spotify"] = dict()
    return data


def get_spotify(now_playing_json):
    # Check if multiple artists, use first to improve search results
    artist = str(now_playing_json["artist"])
    artist_list = artist.split("/")
    if len(artist_list) > 1:
        srch_artist = artist_list[0]
    else:
        srch_artist = artist

    # Check if song length is at max capacity from SXM API (35) and remove the last word to match Spotify API
    srch_title = song_scrub.length_verification(now_playing_json["title"])

    # Escape some troublesome characters, but don"t over-escape and miss searches
    if re.search(r"[*]", srch_title):
        srch_title = re.escape(srch_title)

    # Search Spotify (requests has been flaky in my tests, retry if failed)
    for i in range(0, 3):
        try:
            # results = spotify_api.search(q="artist:" + srch_artist + " track:" + srch_title, limit=1, type="track")
            results = spotify_api.search(q=srch_artist + " " + srch_title, limit=1, type="track")
        except:
            logger.error("There was an error reaching Spotify WEB API. Retrying: " + str(i + 1))
            time.sleep(5)
            continue
        break

    # If found add it
    if results["tracks"]["total"] > 0:
        logger.info("Adding Spotify: " + str(now_playing_json["artist"]) + " - " + str(now_playing_json["title"]))
        spotify_track = results["tracks"]["items"][0]

        # Artist
        delim = ""
        spotify_artists = ""
        for artist in spotify_track["artists"]:
            spotify_artists += delim
            spotify_artists += artist["name"]
            delim = ", "

        now_playing_json["spotify"]["artist"] = spotify_artists
        # Title
        now_playing_json["spotify"]["title"] = spotify_track["name"]
        # URL
        now_playing_json["spotify"]["url"] = spotify_track["external_urls"]["spotify"]
        # URI
        now_playing_json["spotify"]["uri"] = spotify_track["uri"]
        # Album
        now_playing_json["spotify"]["album"] = spotify_track["album"]["name"]
        # Album Image
        if len(spotify_track["album"]["images"]) > 0:
            now_playing_json["spotify"]["album_image"] = spotify_track["album"]["images"][0]["url"]

        return now_playing_json
    else:
        logger.info("No Spotify Found: " + srch_artist + " (" + str(now_playing_json["artist"]) + ") - " +
                    srch_title + " (" + str(now_playing_json["title"]) + ")")
        return now_playing_json
