from decouple import config

DATA_DIR = config('DATA_DIR')


class DirStructureRingConnector():
    def __init__(self, dataDir = DATA_DIR):
        self.unprocessedEvents = dataDir + "/events/unprocessed"
        self.processedEvents = dataDir + "/events/processed"

DEFAULT_DIR_STUCTURE = DirStructureRingConnector()