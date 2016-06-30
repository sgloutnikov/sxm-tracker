import json
from pymongo import MongoClient
from api import api_manager
from db import db_manager

'''Tools script for one time usage/cases'''

FILE_NAME = 'full_sample_data.json'
MONGODB_URI = 'mongodb://localhost:27017/sxm'


# Transform dumped data to JSON array
def convertToJSONArray():
    file = open(FILE_NAME)
    lines = file.readlines()
    file.close()
    newlines = []
    for line in lines[:-1]:
        newlines.append(line.rstrip() + ',\n')
    newlines.append(lines[-1])
    newlines.insert(0, '[\n')
    newlines.append(']')
    file = open(FILE_NAME + '_array', 'w')
    file.writelines(newlines)
    file.close()


# Now run some goodies
def writeArtistSongFile():
    file = open(FILE_NAME + '_array')
    jsondata = json.load(file)
    file.close()
    songs = []

    for line in jsondata:
        try:
            artist = line['channelMetadataResponse']['metaData']['currentEvent']['artists']['name']
            song = line['channelMetadataResponse']['metaData']['currentEvent']['song']['name']
            datastring = repr(artist) + ' - ' + repr(song) + "\n"
            songs.append(datastring)
        except KeyError:
            pass

    file = open('full_sample_songs', 'w')
    file.writelines(songs)
    file.close()


def backFillSampleData():
    file = open(FILE_NAME + '_array')
    jsondata = json.load(file)
    file.close()
    for line in jsondata:
        if line['channelMetadataResponse']['messages']['code'] != 305:
            current = api_manager.extract_now_playing_data(line)
            last = db_manager.get_last_streamed()
            if current['artist'] != last['artist'] and current['song'] != last['song']:
                db_manager.save_new(current)


def insertDummyRecord():
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    data = {}
    data['artist_id'] = ''
    data['artist'] = 'Some Artist'
    data['song_id'] = ''
    data['song'] = 'Some Song Name'
    data['album'] = 'Some Album Name'
    data['startTime'] = '2016-06-29T16:06:23.016Z'
    db.nowplaying.insert_one(data)


#insertDummyRecord()
#backFillSampleData()
