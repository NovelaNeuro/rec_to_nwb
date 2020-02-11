import logging.config
import os

import pandas as pd
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.managers.timestamps_manager_interface import TimestampManagerInterface

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PosTimestampManager(TimestampManagerInterface):
    # override
    def __get_timestamps(self, dataset_num):
        pos_online = readTrodesExtractedDataFile(self.directories[dataset_num][0])
        position = pd.DataFrame(pos_online['data'])
        timestamps = position.time.to_numpy(dtype='int64')
        return timestamps

    # override
    def read_data(self, dataset_num):
        timestamps = self.__get_timestamps(dataset_num)
        continuous_time_dict = self.__get_continuous_time_dict(dataset_num)
        converted_timestamps = self.__convert_timestamps(continuous_time_dict, timestamps)
        return converted_timestamps

    # override
    def get_final_data_shape(self):
        return sum(self.file_lenghts_in_datasets),
