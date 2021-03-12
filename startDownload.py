#!/usr/bin/env python3

import logging
import datetime
import sys


from ringConnector import core

logging.getLogger().setLevel(logging.INFO)
devices = core.listAllDevices()
logging.info(f"found devices {devices}")


print ('Argument List:', str(sys.argv))
if len(sys.argv) > 1:
    dayToDownloadParam = sys.argv[1]
    logging.info(f"will download {dayToDownloadParam}")
    dayToDownload = datetime.datetime.strptime(dayToDownloadParam, '%Y-%m-%d').date()
    res = core.downloadDaysDingVideos(dayToDownload = dayToDownload)
else:
    logging.info('will download today')
    res = core.downloadDaysDingVideos()
 

logging.info(res)