import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from fl.datamigration.processing.continuous_time_extractor import ContinuousTimeExtractor
from fl.datamigration.processing.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AnalogExtractor:

    @staticmethod
    def extract_analog_for_single_dataset(analog_files, continuous_time_file):
        single_dataset_data = {}
        continuous_time_dict = ContinuousTimeExtractor.get_continuous_time_dict_file(continuous_time_file)
        for analog_file in analog_files:
            if 'analog' in analog_file:
                try:
                    analog_data = readTrodesExtractedDataFile(analog_files[analog_file])
                    values = analog_data['data']
                    single_dataset_data[analog_file] = values
                except KeyError as error:
                    pass
                    # message = "there is no " + str(analog_file) + ", error: "
                    # logger.exception(message + str(error))
                except TypeError as error:
                    pass
                    # message = "there is no data for event " + str(analog_file) + ", error: "
                    # logger.exception(message + str(error))
            elif 'timestamp' in analog_file:
                try:
                    timestamp = readTrodesExtractedDataFile(analog_files[analog_file])
                    keys = AnalogExtractor.__convert_keys(continuous_time_dict, timestamp['data'])
                    single_dataset_data[analog_file] = keys
                except KeyError as error:
                    pass
                    # message = "there is no " + str(analog_file) + ", error: "
                    # logger.exception(message + str(error))
                except TypeError as error:
                    pass
                    # message = "there is no data for event " + str(analog_file) + ", error: "
                    # logger.exception(message + str(error))

        return single_dataset_data

    @staticmethod
    def __convert_keys(continuous_time_dict, keys):
        converted_timestamps = TimestampConverter.convert_timestamps(continuous_time_dict, keys)
        return converted_timestamps
