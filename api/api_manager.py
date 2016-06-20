from datetime import datetime, timedelta
import urllib.request
import json
import requests
import re
from db import db_manager


baseurl = 'https://www.siriusxm.com/metadata/pdt/en-us/json/channels/hotjamz/timestamp/'
dummyjson = {'channelMetadataResponse': {'metaData': {'channelName': 'The Heat', 'channelId': 'hotjamz', 'version': 1.1, 'channelNumber': 46, 'dateTime': '2016-06-20T10:03:02.353Z', 'currentEvent': {'startTime': '2016-06-20T10:01:33Z', 'song': {'id': '', 'album': {'name': 'Islah'}, 'creativeArts': [{'size': 'THUMBNAIL', 'encrypted': False, 'url': 'Live/Default/DefaultMDS_t_46.jpg', 'type': 'IMAGE'}, {'size': 'SMALL', 'encrypted': False, 'url': 'Live/Default/DefaultMDS_s_46.jpg', 'type': 'IMAGE'}, {'size': 'MEDIUM', 'encrypted': False, 'url': 'Live/Default/DefaultMDS_m_46.jpg', 'type': 'IMAGE'}, {'size': 'LARGE', 'encrypted': False, 'url': '', 'type': 'IMAGE'}, {'type': 'BIO', 'encrypted': False, 'url': ''}, {'type': 'REVIEWS', 'encrypted': False, 'url': ''}, {'size': 'THUMBNAIL', 'encrypted': True, 'url': 'NY_Assets_1/Default_Content/5_DefaultMDS_t_46.jpg', 'type': 'IMAGE'}, {'size': 'SMALL', 'encrypted': True, 'url': 'NY_Assets_1/Default_Content/5_DefaultMDS_s_46.jpg', 'type': 'IMAGE'}, {'size': 'MEDIUM', 'encrypted': True, 'url': 'NY_Assets_1/Default_Content/5_DefaultMDS_m_46.jpg', 'type': 'IMAGE'}, {'size': 'LARGE', 'encrypted': True, 'url': '', 'type': 'IMAGE'}, {'type': 'BIO', 'encrypted': True, 'url': ''}, {'type': 'REVIEWS', 'encrypted': True, 'url': ''}], 'name': 'Really Really', 'composer': ''}, 'epgInfo': {'segment': {'startTime': '2016-06-20T06:00:00Z', 'description': 'Even when she was in elementary school, Deja Vu wanted to be a DJ. Now she stays up late on school nights, blazing R&B hits from Ciara, Chris Brown, Drake and more on The Heat.', 'duration': 21600, 'segmentId': 3151306}, 'program': {'startTime': '2016-06-20T06:00:00Z', 'live': False, 'description': 'Even when she was in elementary school, Deja Vu wanted to be a DJ. Now she stays up late on school nights, blazing R&B hits from Ciara, Chris Brown, Drake and more on The Heat.', 'title': 'The Heat with Deja Vu', 'firstRun': False, 'episodes': {'startTime': '2016-06-20T06:00:00Z', 'episodeId': 3151306, 'description': 'Even when she was in elementary school, Deja Vu wanted to be a DJ. Now she stays up late on school nights, blazing R&B hits from Ciara, Chris Brown, Drake and more on The Heat.', 'title': 'The Heat with Deja Vu', 'duration': 21600, 'firstRun': False, 'showId': 1069}, 'showId': 1069}}, 'baseUrl': 'http://www.siriusxm.com/albumart/', 'artists': {'id': '', 'name': 'Kevin Gates'}, 'keyValue': '12345678901234567890123456789012', 'siriusXMId': 347750021, 'keyIndex': 5}}, 'status': 1, 'messages': {'message': 'Successful request', 'code': 100}}}


def api_call():
    timenow = (datetime.utcnow() - timedelta(minutes=1)).strftime('%m-%d-%H:%M:00')
    url = baseurl + timenow

    r = requests.get(url)
    jsondata = r.json()
    print(jsondata)


#api_call()

namestring = 'Colonel Loud\/Ricco Barrino'
namestring.replace('\\', '+')
print(namestring)
