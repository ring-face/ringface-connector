#!/usr/bin/env python3

import logging

from ringConnector import core
from ringConnector.dirStructure import DEFAULT_DIR_STUCTURE

logging.getLogger().setLevel(logging.INFO)
devices = core.listAllDevices()
logging.info(f"found devices {devices}")


res = core.downloadDaysDingVideos(dirStructure=DEFAULT_DIR_STUCTURE)
logging.info(res)