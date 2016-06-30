import logging
from datetime import datetime, timedelta
import requests
import json

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
