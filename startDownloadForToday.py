#!/usr/bin/env python3

import logging

from ringConnector import core

logging.getLogger().setLevel(logging.INFO)
devices = core.listAllDevices()
logging.info(f"found devices {devices}")


res = core.downloadDaysDingVideos()
logging.info(res)