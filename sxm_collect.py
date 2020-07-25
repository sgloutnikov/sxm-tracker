import sys

from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
import os
import configparser
from datetime import datetime, timedelta
from db import db_manager
from api import api_manager
from scrubber import scrub_manager


log_config = os.path.join(os.path.dirname(__file__), "logging_config.ini")
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


def collect_now_playing(station, api_url):
    resp, full_json = api_manager.get_now_playing_data(api_url)
    if resp.status_code == 200:
        # TODO: Verify content dict has data available. If not, no data is available from station
        current_np = api_manager.extract_now_playing_data(full_json)
        last_playing = db_manager.get_last_streamed(station)
        current_artist = str(current_np["artist"])
        current_title = str(current_np["title"])
        last_artist = str(last_playing["artist"])
        last_title = str(last_playing["title"])
        if (current_artist != last_artist) and (current_title != last_title):
            logger.info("[" + station + "] - " + "New Song Detected: " +
                        str(current_np["artist"]) + " - " + str(current_np["title"]))
            if scrub_manager.is_clean(station, current_np["artist"], current_np["title"]):
                current_np = scrub_manager.scrub_artist(station, current_np)
                current_np = scrub_manager.scrub_title(station, current_np)
                current_np = api_manager.get_spotify(current_np)
                db_manager.save_new(station, current_np)
            else:
                logger.info("[" + station + "] - " + "-- Skipping: " + current_np["artist"]
                            + " - " + current_np["title"])
    else:
        logger.error("[" + station + "] - " + "Error SXM API: " + resp.status_code + " " +
                     str(resp.content))


if __name__ == "__main__":
    logger.info("Starting Now Playing Collection")
    config = configparser.ConfigParser()
    config.read("sxm_collect_config.ini")
    scheduler = BlockingScheduler()

    # TODO: New SXM API supports requesting multiple channels with one call
    # The Heat
    theheat = "theheat"
    theheat_api_url = config[theheat]["api_url"]
    db_manager.check_init_db(theheat)
    scrub_manager.init(theheat)

    scheduler.add_job(collect_now_playing, kwargs={"station": theheat, "api_url": theheat_api_url},
                      next_run_time=datetime.now(), trigger="interval", seconds=60)

    # The Highway
    thehighway = "thehighway"
    thehighway_api_url = config[thehighway]["api_url"]
    db_manager.check_init_db(thehighway)
    scrub_manager.init(thehighway)
    scheduler.add_job(collect_now_playing, kwargs={"station": thehighway, "api_url": thehighway_api_url},
                      next_run_time=(datetime.now() + timedelta(seconds=30)), trigger="interval", seconds=60)

    scheduler.start()
