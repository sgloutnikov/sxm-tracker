from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
from db import db_manager
from api import api_manager


logging.config.fileConfig('logging_config.ini', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def collect_full_sample_data():
    jsondata = api_manager.get_now_playing_data()
    db_manager.save_full_sample_data(jsondata)


def collect_now_playing():
    # TODO: Look into Redis Queue (http://python-rq.org)
    fulljson = api_manager.get_now_playing_data()
    if fulljson['channelMetadataResponse']['messages']['code'] != 305:
        current = api_manager.extract_now_playing_data(fulljson)
        last = db_manager.get_last_streamed()
        if current['artist'] != last['artist'] and current['song'] != last['song']:
            db_manager.save_new(current)
    else:
        logging.error("Error from API call. " + fulljson['channelMetadataResponse']['messages']['code'] +
                      " " + fulljson['channelMetadataResponse']['messages']['message'])

if __name__ == "__main__":
    logger.info("Starting Now Playing Collection")
    logger.info("Checking Database")
    db_manager.check_init_db()

    # TODO: When in django, probably will have to move to BackgroundScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_now_playing, 'interval', seconds=45)
    scheduler.start()

