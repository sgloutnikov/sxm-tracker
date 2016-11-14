from django.shortcuts import render
import os
from pymongo import MongoClient, DESCENDING
from dateutil import parser
from datetime import datetime, timezone
import urllib.parse


MONGODB_URI = os.environ.get('MONGODB_URI')

client = MongoClient(MONGODB_URI)
db = client.get_default_database()


# Now Playing Page View
def nowplaying(request, page):
    songs = get_now_playing(page)
    songDict = {}
    id = 1
    for song in songs:
        songDict[id] = song
        songDict[id]['timeago'] = get_time_ago_string(str(song['startTime']))
        songDict[id]['ytlink'] = get_youtube_link(song)
        id += 1
    songDict['page'] = page
    return render(request, 'theheat/nowplaying.html', {'songs': songDict})


def get_now_playing(page):
    skip = int(page) - 1
    songs = db.nowplaying.find({}).sort("startTime", direction=DESCENDING).limit(16).skip((skip * 16))
    return songs


def get_time_ago_string(song_time_string):
    tsthen = parser.parse(song_time_string)
    tsnow = datetime.now(timezone.utc)
    delta_seconds = (tsnow - tsthen).total_seconds()
    m, s = divmod(delta_seconds, 60)
    h, m = divmod(m, 60)

    time_ago = ''
    if h > 0:
        if h == 1:
            time_ago += "1 hour ago"
            return time_ago
        else:
            time_ago += str(round(h))
            time_ago += " hours ago"
            return time_ago
    if m > 0:
        if m == 0:
            time_ago += "1 minute ago"
            return time_ago
        else:
            time_ago += str(round(m))
            time_ago += " minutes ago"
            return time_ago
    if s > 0:
        time_ago += str(round(s))
        time_ago += " seconds ago"
        return time_ago


def get_youtube_link(song_json):
    yt_link = "https://www.youtube.com/results?search_query="

    artist = str(song_json['artist'])
    srch_song = str(song_json['song'])
    srch_artist = artist.replace('/', ' ')

    yt_link += urllib.parse.quote_plus(srch_artist)
    yt_link += '+'
    yt_link += urllib.parse.quote_plus(srch_song)
    return yt_link
