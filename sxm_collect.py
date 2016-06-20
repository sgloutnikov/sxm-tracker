from apscheduler.schedulers.blocking import BlockingScheduler
import time
import logging.config

logging.config.fileConfig('logging_config.ini')
logger = logging.getLogger(__name__)


def timed_job():
    print('Work Work!')
    logger.info("Log Work")
    more_work()


def more_work():
    time.sleep(3)
    print("More Work...")
    logger.info("Log More Work")


if __name__ == "__main__":
    logger.info("Starting")
    scheduler = BlockingScheduler()
    scheduler.add_job(timed_job, 'interval', seconds=30)
    scheduler.start()
