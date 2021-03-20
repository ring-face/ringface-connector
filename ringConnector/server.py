import logging
from flask import Flask, jsonify, request
from ringConnector.core import downloadDaysDingVideos
import datetime


app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)
logging.info("Server started")


@app.route('/')
def hello():
    return 'Pong'

@app.route('/connector/download/today')
def downloadForToday():
    eventsList = downloadDaysDingVideos()
    return jsonify(eventsList)

@app.route('/connector/download/<dayString>', methods=["POST"])
def downloadForDay(dayString):
    downloadedEventsRingIds = request.json

    # assert dayString == request.view_args['day']
    
    dayToDownload = datetime.datetime.strptime(dayString, '%Y%m%d').date()

    eventsList = downloadDaysDingVideos(dayToDownload = dayToDownload, downloadedEventsRingIds = downloadedEventsRingIds)
    return jsonify(eventsList)
