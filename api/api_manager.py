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
    data = {'artist': {}, 'song': {}}
    data['artist']['id'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['artists']['id']
    data['artist']['name'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['artists']['name']
    data['song']['id'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['id']
    data['song']['name'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['name']
    data['song']['albumName'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['song']['album']['name']
    data['startTime'] = full_json['channelMetadataResponse']['metaData']['currentEvent']['startTime']
    return data
