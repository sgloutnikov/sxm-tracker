from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


def collect_trigger():
    # TODO: Look into Redis Queue (http://python-rq.org)
    logger.info("Log Work Work!")


if __name__ == "__main__":
    # TODO: When in django, probably will have to move to BackgroundScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_trigger, 'interval', seconds=30)
    scheduler.start()

