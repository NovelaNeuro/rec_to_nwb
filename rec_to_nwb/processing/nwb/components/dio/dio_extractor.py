import logging.config
import os
# import numpy as np

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    @staticmethod
    def extract_dio_for_single_dataset(filtered_files, continuous_time_file,
                                        convert_timestamps=True):
        single_dataset_data = {}
        continuous_time = ContinuousTimeExtractor.get_continuous_time_array_file(continuous_time_file)

        for dio_sensor in filtered_files:
            try:
                dio_data = readTrodesExtractedDataFile(filtered_files[dio_sensor])
                # dio_data['data'] is a labeled array with 'time' and 'state' columns. 'time' corresponds to sample count
                single_dataset_data[dio_sensor] = DioExtractor.__get_dio_time_series(
                        dio_data, continuous_time, convert_timestamps)
                # keys, values = DioExtractor.__get_dio_time_series(dio_data, continuous_time_dict
                # single_dataset_data[dio_sensor] = ([keys, values])

            except KeyError as error:
                message = "there is no " + str(dio_sensor) + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_sensor) + ", error: "
                logger.exception(message + str(error))
        return single_dataset_data

    @staticmethod
    def __get_dio_time_series(dio_data, continuous_time, convert_timestamps=True):
        dio_state = dio_data['data']['state']
        time_counts = dio_data['data']['time'] # time sample counts
        if not convert_timestamps:
            return [time_counts, dio_state]
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time, time_counts)
        #values = np.asarray(dio_data['state'], dtype='bool')
        # values = [bool(recorded_event[1]) for recorded_event in dio_data['data']]
        # keys = [recorded_event[0] for recorded_event in dio_data['data']]
        # keys = DioExtractor.__convert_keys(continuoues_time_dict, keys)
        # return keys, values
        return [converted_timestamps, dio_state]

    # @staticmethod
    # def __convert_keys(continuous_time_array, keys):
    #     converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_array, keys)
    #     return converted_timestamps
