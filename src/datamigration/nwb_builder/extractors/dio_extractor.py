import concurrent.futures
import logging
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager
from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    def __init__(self, datasets, dio_metadata):
        self.datasets = datasets
        self.dio_manager = DioManager(datasets, dio_metadata)
        self.filtered_dio_files = self.dio_manager.get_dio_files()
        self.dio_metadata = dio_metadata
        self.continuous_time_extractor = ContinuousTimeExtractor()

    def get_dio(self):
        return self.__extract_dio_for_single_dataset()

    def _extract_dio(self):
        all_dio_data = []
        threads = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for i in range(len(self.datasets)):
                threads.append(executor.submit(self.__extract_dio_for_single_dataset(self.filtered_dio_files[i])))
        for i in range(len(self.datasets)):
            all_dio_data.extend(threads[i].result())

    def __extract_dio_for_single_dataset(self, filtered_files):
        all_dio_data = []
        for dio_file in filtered_files:
            try:
                dio_data = readTrodesExtractedDataFile(dio_file)
                keys, values = self.__build_dio_time_series(dio_data)
                all_dio_data.append([keys, values])

            except KeyError as error:
                message = "there is no " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
            except TypeError as error:
                message = "there is no data for event " + str(dio_file) + ", error: "
                logger.exception(message + str(error))
        return all_dio_data

    def __build_dio_time_series(self, dio_data):

        values = [recorded_event[1] for recorded_event in dio_data['data']]
        keys = self.__dio_keys_conversion(dio_data)
        return keys, values

    def __dio_keys_conversion(self, dio_data):
        keys = [recorded_event[0] for recorded_event in dio_data['data']]
        convertedTimestamps = TimestampConverter.convert_timestamps(self.continuous_time_dict, keys)
        keys = convertedTimestamps
        return keys
