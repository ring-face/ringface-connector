from decouple import config

DATA_DIR = config('DATA_DIR')


class DirStructure():
    def __init__(self, dataDir = DATA_DIR):
        self.videos = dataDir + "/videos"

DEFAULT_DIR_STUCTURE = DirStructure()