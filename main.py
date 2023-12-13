import datetime
import logging
from flask import jsonify
from ringConnector.core import downloadDaysDingVideos

def setup_logging():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('requests_oauthlib').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.info("Logging set up")


def download(request):
    logging.debug(f"Download triggered")
    try:

        dayToDownload = request.args.get('dayToDownload', default=None, type=str)

        eventsList = None
        if dayToDownload is None:
            logging.debug(f"Downloading events for today")
            eventsList = downloadDaysDingVideos()
        else:
            dayToDownload = datetime.datetime.strptime(dayToDownload, '%Y%m%d').date()

            downloadedEventsRingIds = request.json
            logging.debug(f"Downloading {dayToDownload}. Will not re-download events {downloadedEventsRingIds}")
            eventsList = downloadDaysDingVideos(dayToDownload=dayToDownload, downloadedEventsRingIds = downloadedEventsRingIds)

        return jsonify(eventsList)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": f"An error occurred: {e}"}), 500
    
setup_logging()