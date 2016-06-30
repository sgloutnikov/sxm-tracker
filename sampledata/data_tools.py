import json
from pymongo import MongoClient

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
    pass


def insertDummyRecord():
    client = MongoClient(MONGODB_URI)
    db = client.get_default_database()
    data = {'artist': {}, 'song': {}}
    data['artist']['id'] = ''
    data['artist']['name'] = 'Some Artist'
    data['song']['id'] = ''
    data['song']['name'] = 'Some Song Name'
    data['song']['albumName'] = 'Some Album Name'
    data['startTime'] = '2016-06-29T16:06:23.016Z'
    db.nowplaying.insert_one(data)

