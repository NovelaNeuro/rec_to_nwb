import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FileSorter:

    @staticmethod
    def sort_filenames(filenames):
        filenames.sort(key=lambda item: (len(item), item))
        return filenames
