import logging.config
import os

import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from fldatamigration.processing.nwb.common.timestamps_manager import TimestampManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosTimestampManager(TimestampManager):
    def __init__(self, directories, continuous_time_directories):
        TimestampManager.__init__(self, directories, continuous_time_directories)

    # override
    def _get_timestamps(self, dataset_id):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][0])
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')
