import logging
from datetime import datetime, timedelta
import requests

logger = logging.getLogger(__name__)

baseurl = 'https://www.siriusxm.com/metadata/pdt/en-us/json/channels/hotjamz/timestamp/'


def get_now_playing_data():
    timenow = (datetime.utcnow() - timedelta(minutes=1)).strftime('%m-%d-%H:%M:00')
    url = baseurl + timenow
    r = requests.get(url)
    jsondata = r.json()
    return jsondata

