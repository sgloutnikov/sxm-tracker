import os
import threading
import time

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import logging.config
import os
import configparser
from datetime import datetime, timedelta
from db import db_manager
from api import api_manager
from scrubber import scrub_manager
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

log_config = os.path.join(os.path.dirname(__file__), "logging_config.ini")
logging.config.fileConfig(log_config, disable_existing_loggers=False)
logger = logging.getLogger(__name__)


# HTTP Server to allow ping and prevention of Heroku dyno sleeping
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'It works!')

    def do_HEAD(self):
        self.send_response(200)
        self.end_headers()


def collect_now_playing(api_url, station_list):
    resp, full_json = api_manager.get_now_playing_data(api_url)
    if "channels" not in full_json:
        logger.error("SXM API: Missing channel data in response")
        return
    if resp.status_code == 200:
        # For each station check if data exists and process it
        for station in station_list:
            if station in full_json["channels"]:
                process_station(station, full_json["channels"][station])
                # Artificial sleep just in case not to spam Spotify API if many stations
                time.sleep(5)
            else:
                logger.error("Data missing in API response for " + str(station))
    else:
        logger.error("SXM API: " + resp.status_code + " " + str(resp.content))


def process_station(station, station_json):
    if api_manager.has_song_data(station_json):
        current_np = api_manager.extract_now_playing_data(station_json)
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
        logger.info("[" + station + "] - " + "No song data in API reply")


def prepare_station_data(collection_list):
    for song in collection_list:
        logger.info("DB and Scrub Init: " + str(song))
        db_manager.check_init_db(song)
        scrub_manager.init(song)


if __name__ == "__main__":
    logger.info("Starting sleep prevention HTTPD server")
    # Run a simple HTTP check to be pinged and prevent Heroku dyno from sleeping.
    # PORT is exposed by the Heroku environment
    httpd_port = os.environ.get("PORT")
    httpd = HTTPServer(('', int(httpd_port)), SimpleHTTPRequestHandler)
    thread = threading.Thread(target=httpd.serve_forever)
    thread.daemon = True
    thread.start()

    logger.info("Starting Now Playing Collection")
    config = configparser.ConfigParser()
    config.read("sxm_collect_config.ini")
    scheduler = BlockingScheduler()

    full_api_url = config['api']["url"]
    parsed_url = urlparse(full_api_url)
    parsed_station_list = parse_qs(parsed_url.query)['channels'][0].split(',')
    prepare_station_data(parsed_station_list)
    scheduler.add_job(collect_now_playing,
                      kwargs={"api_url": full_api_url, "station_list": parsed_station_list},
                      next_run_time=datetime.now(), trigger="interval", seconds=60)

    scheduler.start()
