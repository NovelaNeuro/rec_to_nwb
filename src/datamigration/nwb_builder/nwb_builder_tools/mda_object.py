import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class MdaObject:

    def __init__(self, mda_data, mda_timestamps):
        self.mda_data = mda_data
        self.mda_timestamps = mda_timestamps
