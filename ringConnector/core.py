import logging

import json
import os
import sys
from datetime import date
from pathlib import Path
from pprint import pprint
from decouple import config


from ring_doorbell import Ring, Auth

oauthFilePath = config("OAUTH_FILE")
oauth_file = Path(oauthFilePath)


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
    else:
        logging.warn(f"event {eventName} has already been downloaded")

def listAllDevices():

    ring = getRing()

    devices = ring.devices()
    return devices
  

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


def getAuth():
    if oauth_file.is_file():
        auth = Auth("MyProject/1.0", json.loads(oauth_file.read_text()), token_updated)
    else:
        sys.exit(f"Authorization file does not exist {oauthFilePath}")
    return auth

def token_updated(token):
    oauth_file.write_text(json.dumps(token))

def getRing():
    auth = getAuth()
    ring = Ring(auth)
    ring.update_data()
    return ring
