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


def collect_now_playing():
    fulljson = api_manager.get_now_playing_data()
    if fulljson['channelMetadataResponse']['messages']['code'] != 305:
        current = api_manager.extract_now_playing_data(fulljson)
        last = db_manager.get_last_streamed()
        current_artist = str(current['artist'])
        current_song = str(current['song'])
        last_artist = str(last['artist'])
        last_song = str(last['song'])
        if (current_artist != last_artist) and (current_song != last_song):
            logger.info("New Song Detected. " + str(current['artist']) + " - " + str(current['song']))
            if scrub_manager.is_clean(current['artist'], current['song']):
                current = scrub_manager.scrub_artist(current)
                current = scrub_manager.scrub_song(current)
                current = api_manager.get_spotify(current)
                db_manager.save_new(current)
            else:
                logger.info('-- Skipping: ' + current['artist'] + " - " + current['song'])
    else:
        code = str(fulljson['channelMetadataResponse']['messages']['code'])
        message = str(fulljson['channelMetadataResponse']['messages']['message'])
        logger.error("Error from API call. " + code + " " + message)

if __name__ == "__main__":
    logger.info("Starting Now Playing Collection")
    db_manager.check_init_db()
    scrub_manager.init()

    # TODO: When in django, probably will have to move to BackgroundScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_now_playing, 'interval', seconds=45)
    scheduler.start()

