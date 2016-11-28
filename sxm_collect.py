from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
import os
from db import db_manager
from api import api_manager
from scrubber import scrub_manager


log_config = os.path.join(os.path.dirname(__file__), 'logging_config.ini')
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def collect_full_sample_data():
    jsondata = api_manager.get_now_playing_data()
    db_manager.save_full_sample_data(jsondata)


def collect_now_playing(station, api_url):
    fulljson = api_manager.get_now_playing_data(api_url)
    if fulljson['channelMetadataResponse']['messages']['code'] != 305:
        current = api_manager.extract_now_playing_data(fulljson)
        last = db_manager.get_last_streamed(station)
        current_artist = str(current['artist'])
        current_song = str(current['song'])
        last_artist = str(last['artist'])
        last_song = str(last['song'])
        if (current_artist != last_artist) and (current_song != last_song):
            logger.info("[" + station + "] - " + "New Song Detected. " + str(current['artist']) +
                        " - " + str(current['song']))
            if scrub_manager.is_clean(station, current['artist'], current['song']):
                current = scrub_manager.scrub_artist(station, current)
                current = scrub_manager.scrub_song(station, current)
                current = api_manager.get_spotify(current)
                db_manager.save_new(station, current)
            else:
                logger.info("[" + station + "] - " + "-- Skipping: " + current['artist'] + " - " + current['song'])
    else:
        code = str(fulljson['channelMetadataResponse']['messages']['code'])
        message = str(fulljson['channelMetadataResponse']['messages']['message'])
        logger.error("[" + station + "] - " + "Error from API call. " + code + " " + message)

if __name__ == "__main__":
    logger.info("Starting Now Playing Collection")
    db_manager.check_init_db('theheat')
    scrub_manager.init('theheat')

    scheduler = BlockingScheduler()
    scheduler.add_job(collect_now_playing, kwargs={'station': 'theheat',
                'api_url': 'https://www.siriusxm.com/metadata/pdt/en-us/json/channels/hotjamz/timestamp/'},
                      trigger='interval', seconds=45)
    scheduler.start()
