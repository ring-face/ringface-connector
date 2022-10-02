import getpass
from ring_doorbell import Auth
from decouple import config
from pathlib import Path
from oauthlib.oauth2 import MissingTokenError
import logging
import json

oauth_file = Path(config("OAUTH_FILE"))


"""
Asks for the user credentials and creates the oauth json file
"""
def writeAuthFile():

    logging.warn(f"will create new oauth json file at {config('OAUTH_FILE')}")

    username = input("Please enter your ring Username: ")
    password = getpass.getpass("Please enter your ring Password: ")
    auth = Auth("Csabas Ringface", None, token_updated)
    try:
        auth.fetch_token(username, password)
    except MissingTokenError:
        auth.fetch_token(username, password, otp_callback())


def token_updated(token):
    oauth_file.write_text(json.dumps(token))
    logging.warn(f"new token file created")


def otp_callback():
    auth_code = input("Please enter your 2FA code that was sent to you: ")
    return auth_code

