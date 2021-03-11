import logging
from flask import Flask, jsonify
from ringConnector.core import downloadDaysDingVideos


app = Flask(__name__)
logging.getLogger().setLevel(logging.INFO)
logging.info("Server started")


@app.route('/')
def hello():
    return 'Pong'

@app.route('/conector/download/today')
def downloadForToday():
    eventsList = downloadDaysDingVideos()
    return jsonify(eventsList)
