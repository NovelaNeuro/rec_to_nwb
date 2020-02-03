import logging.config
import os
from pathlib import Path

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class RecFileFinder:

    def __init__(self):
        pass

    @staticmethod
    def find_rec_files(path):
        rec_files = []
        for file_path in Path(path).glob('**/*.rec'):
            rec_files.append(file_path)
        return rec_files
