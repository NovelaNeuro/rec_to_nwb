import logging.config
import os

import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosTimestampManager(TimestampManagerInterface):
    def __init__(self, directories, continuous_time_directories):
        TimestampManagerInterface.__init__(self, directories, continuous_time_directories)

    # override
    def _get_timestamps(self, dataset_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')
