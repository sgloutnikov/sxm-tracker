from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
from db import db_manager
from api import api_manager


logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


def collect_now_playing():
    # TODO: Look into Redis Queue (http://python-rq.org)
    logger.info("Log Work Work!")


def collect_full_sample_data():
    jsondata = api_manager.get_now_playing_data()
    db_manager.save_full_sample_data(jsondata)

if __name__ == "__main__":
    logger.info("Starting Full Sample Data Dump")
    # Dump full sample data every 120s for analysis
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_full_sample_data, 'interval', seconds=120)
    scheduler.start()

    """
    # TODO: When in django, probably will have to move to BackgroundScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_now_playing, 'interval', seconds=30)
    scheduler.start()
    """

