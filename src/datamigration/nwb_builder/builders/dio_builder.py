import logging.config
import os

from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_files import DioFiles
from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioBuilder:

    def __init__(self):
        self.dio_files = DioFiles()
        self.timestamp_converter = TimestampConverter()

    def build_for_single_dataset(self, continuous_time_dict, dataset, all_dio_timeseries):
        dio_dict = self.dio_files.get_dio_dict(dataset.get_data_path_from_dataset('DIO'))
        for dio_time_series in all_dio_timeseries:
            try:
                dio_data = readTrodesExtractedDataFile(dataset.get_data_path_from_dataset('DIO') +
                                                       dio_dict[dio_time_series['name']])

                keys, values = self.__build_dio_time_series(continuous_time_dict, dio_data)
                dio_time_series["dio_values"] = values
                dio_time_series["dio_timestamps"] = keys

            except KeyError as error:
                message = "there is no " + str(dio_time_series['name']) + " file" + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_time_series['name'] + ", error: ")
                logger.exception(message + str(error))

    def __build_dio_time_series(self, continuous_time_dict, dio_data):

        values = [recorded_event[1] for recorded_event in dio_data['data']]
        keys = self.__dio_keys_conversion(continuous_time_dict, dio_data)
        return keys, values

    def __dio_keys_conversion(self, continuous_time_dict, dio_data):
        keys = [recorded_event[0] for recorded_event in dio_data['data']]
        convertedTimestamps = self.timestamp_converter.convert_timestamps(continuous_time_dict, keys)
        keys = convertedTimestamps
        return keys
