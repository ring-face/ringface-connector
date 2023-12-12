import logging
from flask import jsonify
from ringConnector.core import downloadDaysDingVideos

def setup_logging():
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.DEBUG)
    logging.getLogger('requests_oauthlib').setLevel(logging.INFO)
    logging.getLogger('urllib3').setLevel(logging.INFO)
    logging.info("Logging set up")


def downloadForToday(request):
    try:
        logging.debug(f"Downloading todays events")
        eventsList = downloadDaysDingVideos()
        return jsonify(eventsList)
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": f"An error occurred: {e}"}), 500
    
setup_logging()