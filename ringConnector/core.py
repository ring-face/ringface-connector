import logging
import json
import os
import sys
from datetime import date
from pathlib import Path
from pprint import pprint
from decouple import config

from ring_doorbell import Ring, Auth

from ringConnector.dirStructure import DEFAULT_DIR_STUCTURE


oauthFilePath = config("OAUTH_FILE")
oauth_file = Path(oauthFilePath)


def downloadDaysDingVideos(dayToDownload=date.today(), dirStructure=DEFAULT_DIR_STUCTURE, downloadedEventsRingIds = []):

    logging.debug(f"exising events will not be downloaded: {downloadedEventsRingIds}")
    ring = getRing()

    downloadedEvents = []

    logging.info(f"Importing all ding event videos for {dayToDownload}")
    devices = ring.devices()
    for doorbell in devices['doorbots']:
        for event in doorbell.history(limit=100, kind='ding'):
            if (dayToDownload == None or event['created_at'].date() == dayToDownload) and event["id"] in downloadedEventsRingIds:
                eventJson = downloadAndSaveEvent(event, doorbell, dirStructure, dayToDownload)
                downloadedEvents.append(eventJson)

    return downloadedEvents

def downloadAndSaveEvent(event, doorbell, dirStructure, dayToDownload):

    logging.debug(f"will download video for event {event}")


    id  = event['id'] 
    eventName = event['created_at'].strftime("%Y%m%d-%H%M%S")

    filename = f"{dirStructure.videos}/{eventName}"
    videoFileName = filename+".mp4" 

    eventJson = {
        'ringId':id, 
        'date': dayToDownload.strftime("%Y%m%d"),
        'eventName': eventName,
        'createdAt':event['created_at'].strftime('%Y-%m-%dT%H:%M:%S.%fZ'), #json formatted event time
        'answered': event['answered'], 
        'kind': event['kind'], 
        'duration': event['duration'],
        'videoFileName': videoFileName,
        'status': 'UNPROCESSED'
    }
    with open(filename + ".json", 'w') as eventDetails:
        json.dump(eventJson, eventDetails)

    doorbell.recording_download(id,filename=videoFileName,override=True)

    return eventJson

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
