from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
from api import api_manager

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


def collect_now_playing():
    # TODO: Look into Redis Queue (http://python-rq.org)
    logger.info("Log Work Work!")


def collect_full_api_data():
    pass

if __name__ == "__main__":
    # TODO: When in django, probably will have to move to BackgroundScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_now_playing, 'interval', seconds=30)
    scheduler.start()

