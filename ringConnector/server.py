import logging
from flask import Flask, jsonify, request
from ringConnector.core import downloadDaysDingVideos
import datetime

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)
logging.getLogger('requests_oauthlib').setLevel(logging.INFO)
logging.getLogger('urllib3').setLevel(logging.INFO)

app = Flask(__name__)


logging.info("Server started")


@app.route('/')
def hello():
    return 'Pong'

@app.route('/connector/download/today')
def downloadForToday():
    logging.debug(f"Downloading todays events")
    eventsList = downloadDaysDingVideos()
    return jsonify(eventsList)

@app.route('/connector/download/<dayString>', methods=["POST"])
def downloadForDay(dayString):
    downloadedEventsRingIds = request.json
    logging.debug(f"Downloading {dayString}. Will not re-download events {downloadedEventsRingIds}")

    # assert dayString == request.view_args['day']
    
    dayToDownload = datetime.datetime.strptime(dayString, '%Y%m%d').date()

    eventsList = downloadDaysDingVideos(dayToDownload = dayToDownload, downloadedEventsRingIds = downloadedEventsRingIds)

    logging.debug(f"downloaded {len(eventsList)} new events for {dayToDownload}")

    return jsonify(eventsList)
