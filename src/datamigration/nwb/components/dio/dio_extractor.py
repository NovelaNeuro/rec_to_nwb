import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:
    def extract_dio_for_single_dataset(self, filtered_files, continuoues_time_dict):
        single_dataset_data = {}
        for dio_file in filtered_files:
            try:
                dio_data = readTrodesExtractedDataFile(filtered_files[dio_file])
                keys, values = self.__get_dio_time_series(dio_data, continuoues_time_dict)
                single_dataset_data[dio_file] = ([keys, values])

            except KeyError as error:
                message = "there is no " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
        return single_dataset_data

    def __get_dio_time_series(self, dio_data, continuoues_time_dict):

        values = [recorded_event[1] for recorded_event in dio_data['data']]
        keys = [recorded_event[0] for recorded_event in dio_data['data']]
        keys = self.__convert_keys(continuoues_time_dict, keys)
        return keys, values

    def __convert_keys(self, continuous_time_dict, keys):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, keys)
        return converted_timestamps
