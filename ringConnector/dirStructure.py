
DATA_DIR = './data'


class DirStructureRingConnector():
    def __init__(self, unprocessedEvents = DATA_DIR + "/events/unprocessed", processedEvents = DATA_DIR + "/events/processed"):
        self.unprocessedEvents = unprocessedEvents
        self.processedEvents = processedEvents

DEFAULT_DIR_STUCTURE = DirStructureRingConnector()