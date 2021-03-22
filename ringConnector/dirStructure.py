from decouple import config
from pathlib import Path

DATA_DIR = config('DATA_DIR')


class DirStructure():
    def __init__(self, dataDir = DATA_DIR):
        self.videos = dataDir + "/videos"
        Path(self.videos).mkdir(parents=True, exist_ok=True)


DEFAULT_DIR_STUCTURE = DirStructure()