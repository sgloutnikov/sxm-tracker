from apscheduler.schedulers.blocking import BlockingScheduler
import time


def timed_job():
    print('Work Work!')
    more_work()


def more_work():
    time.sleep(3)
    print("More Work...")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(timed_job, 'interval', seconds=5)
    scheduler.start()
