import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    @staticmethod
    def extract_dio_for_single_dataset(filtered_files, continuous_time_file):
        single_dataset_data = {}
        continuous_time_dict = ContinuousTimeExtractor.get_continuous_time_dict_file(continuous_time_file)
        for dio_file in filtered_files:
            try:
                dio_data = readTrodesExtractedDataFile(filtered_files[dio_file])
                keys, values = DioExtractor.__get_dio_time_series(dio_data, continuous_time_dict)
                single_dataset_data[dio_file] = ([keys, values])

            except KeyError as error:
                message = "there is no " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
        return single_dataset_data

    @staticmethod
    def __get_dio_time_series(dio_data, continuoues_time_dict):

        values = [bool(recorded_event[1]) for recorded_event in dio_data['data']]
        keys = [recorded_event[0] for recorded_event in dio_data['data']]
        keys = DioExtractor.__convert_keys(continuoues_time_dict, keys)
        return keys, values

    @staticmethod
    def __convert_keys(continuous_time_dict, keys):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, keys)
        return converted_timestamps
