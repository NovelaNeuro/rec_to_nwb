import concurrent.futures
import logging
import os

import numpy as np
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    def __init__(self, filtered_dio_files, continuous_time_dicts):
        self.filtered_dio_files = filtered_dio_files
        self.continuous_time_dics = continuous_time_dicts
        self.timestamp_converter = TimestampConverter()

    def get_dio(self):
        return self.__extract_dio()

    def __extract_dio(self):
        all_dio_data = []
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(np.shape(self.filtered_dio_files)[0]):
                threads.append(executor.submit(self.__extract_dio_for_single_dataset,
                                               self.filtered_dio_files[i],
                                               self.continuous_time_dics[i]))
        for thread in threads:
            all_dio_data.extend(thread.result())
        return all_dio_data

    def __extract_dio_for_single_dataset(self, filtered_files, continuous_time_dict):
        all_dio_data = []
        for dio_file in filtered_files:
            try:
                dio_data = readTrodesExtractedDataFile(dio_file)
                keys, values = self.__build_dio_time_series(dio_data, continuous_time_dict)
                all_dio_data.append([keys, values])

            except KeyError as error:
                message = "there is no " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
        return all_dio_data

    def __build_dio_time_series(self, dio_data, continuous_time_dict):
        values = [recorded_event[1] for recorded_event in dio_data['data']]
        keys = self.__dio_keys_conversion(dio_data, continuous_time_dict)
        return keys, values

    def __dio_keys_conversion(self, dio_data, continuous_time_dict):
        keys = [recorded_event[0] for recorded_event in dio_data['data']]
        convertedTimestamps = TimestampConverter.convert_timestamps(continuous_time_dict, keys)
        keys = convertedTimestamps
        return keys
