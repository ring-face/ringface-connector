import logging

import json
import getpass
import os
from datetime import date
from pathlib import Path
from pprint import pprint

from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError


oauth_file = Path("oauth-autorization.json")

def downloadDaysDingVideos(dirStructure, today=date.today()):
    ring = getRing()

    downloadedEvents = []

    logging.info(f"Importing all ding event videos for {today}")
    devices = ring.devices()
    for doorbell in devices['doorbots']:
        for event in doorbell.history(limit=100, kind='ding'):
            if event['created_at'].date() == today:
                downloadAndSaveEvent(event, doorbell, dirStructure)
                downloadedEvents.append(event)

    return downloadedEvents

def downloadAndSaveEvent(event, doorbell, dirStructure):

    logging.debug(f"will download video for event {event}")


    id  = event['id'] 
    eventName = event['created_at'].strftime("%Y%m%d-%H%M%S")
    eventDir = f"{dirStructure.unprocessedEvents}/{eventName}"
    if not os.path.isdir(eventDir):
        os.mkdir(eventDir)

    filename = f"{eventDir}/{id}"

    with open(filename + ".json", 'w') as eventDetails:
        json.dump({'id':id, 'createdAt':eventName, 'answered': event['answered'], 'kind': event['kind'], 'duration': event['duration']}, eventDetails)


    doorbell.recording_download(id,filename=filename+".mp4",override=True)


def listAllDevices():

    ring = getRing()

    devices = ring.devices()
    return devices

def getEventsBefore(eventId):
    devices = getRing().devices()
    for doorbell in devices['doorbots']:

        # listing the last 15 events of any kind
        for event in doorbell.history(limit=10, older_than=eventId):
            print('ID:       %s' % event['id'])
            print('Kind:     %s' % event['kind'])
            print('Answered: %s' % event['answered'])
            print('When:     %s' % event['created_at'])
            print('--' * 50)
  

def getLastDoorbellEvents(maxEvents=10):
    devices = getRing().devices()
    for doorbell in devices['doorbots']:

        # listing the last 15 events of any kind
        for event in doorbell.history(limit=maxEvents):
            print('ID:       %s' % event['id'])
            print('Kind:     %s' % event['kind'])
            print('Answered: %s' % event['answered'])
            print('When:     %s' % event['created_at'])
            print('--' * 50)

        # get a event list only the triggered by motion
        # events = doorbell.history(kind='motion')



def token_updated(token):
    oauth_file.write_text(json.dumps(token))


def otp_callback():
    auth_code = input("2FA code: ")
    return auth_code

def getAuth():
    if oauth_file.is_file():
        auth = Auth("MyProject/1.0", json.loads(oauth_file.read_text()), token_updated)
    else:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
        auth = Auth("MyProject/1.0", None, token_updated)
        try:
            auth.fetch_token(username, password)
        except MissingTokenError:
            auth.fetch_token(username, password, otp_callback())

    return auth


def getRing():
    auth = getAuth()

    ring = Ring(auth)

    ring.update_data()

    return ring
