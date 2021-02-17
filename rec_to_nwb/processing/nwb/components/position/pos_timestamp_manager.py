import logging.config
import os

import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.nwb.common.timestamps_manager import TimestampManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosTimestampManager(TimestampManager):
    def __init__(self, directories, continuous_time_directories,
                    convert_timestamps=True):
        TimestampManager.__init__(self, directories, continuous_time_directories)
        self.convert_timestamps = convert_timestamps

    # override
    def _get_timestamps(self, dataset_id):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_id][0])
        position = pd.DataFrame(pos_online['data'])
        return position.time.to_numpy(dtype='int64')

    def retrieve_real_timestamps(self, dataset_id):
        return TimestampManager.retrieve_real_timestamps(self, dataset_id,
                                    convert_timestamps=self.convert_timestamps)
