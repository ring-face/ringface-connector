import getpass
from ring_doorbell import Auth
from decouple import config
from pathlib import Path
from oauthlib.oauth2 import MissingTokenError
import logging

oauth_file = Path(config("OAUTH_FILE"))


"""
Asks for the user credentials and creates the oauth json file
"""
def writeAuthFile():

    logging.warn(f"will create new oauth json file at {config('OAUTH_FILE')}")

    username = input("Username: ")
    password = getpass.getpass("Password: ")
    auth = Auth("MyProject/1.0", None, token_updated)
    try:
        auth.fetch_token(username, password)
    except MissingTokenError:
        auth.fetch_token(username, password, otp_callback())


def token_updated(token):
    oauth_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

