import logging
import json
import os
import sys
from datetime import date
import time
from pathlib import Path
from pprint import pprint
from decouple import config
import requests

from ring_doorbell import Ring, Auth

from ringConnector.dirStructure import DEFAULT_DIR_STUCTURE
from ringConnector.gsm import load_ring_auth_json, update_ring_auth_json



def downloadDaysDingVideos(dayToDownload=date.today(), dirStructure=DEFAULT_DIR_STUCTURE, downloadedEventsRingIds = []):

    logging.debug(f"exising events will not be downloaded: {downloadedEventsRingIds}")
    ring = getRing()

    downloadedEvents = []

    logging.info(f"Importing all ding event videos for {dayToDownload}")
    devices = ring.devices()
    for doorbell in devices['doorbots']:
        for event in doorbell.history(limit=300, kind='ding'):
            if (dayToDownload == None or event['created_at'].date() == dayToDownload):
                if str(event["id"]) in downloadedEventsRingIds:
                    logging.debug(f"event {event['id']} already present, will not re-download")
                elif event["recording"]["status"] != "ready":
                    logging.debug(f"event {event['id']} is not yet ready, and can not be downloaded")
                else:
                    logging.debug(f"event {event['id']} will be downloaded")
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
        'ringId':str(id), 
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

    # short after the event, the video is not yet be available for download
    # on unavailablility retry for 100 sec
    i = 1
    while True:
        try:
            doorbell.recording_download(id,filename=videoFileName,override=True)
            break
        except requests.exceptions.HTTPError as err:
            logging.info(f"{videoFileName} is not yet available. will retry in 10 sec. Err: {err.response.status_code}")
            i = i + 1
            if i == 10:
                break
            else:
                time.sleep(10)

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
    auth = Auth("Ringface/v1", load_ring_auth_json(), update_ring_auth_json)
    return auth


def getRing():
    auth = getAuth()
    ring = Ring(auth)
    ring.update_data()
    return ring
