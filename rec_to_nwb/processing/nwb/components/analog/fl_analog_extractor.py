import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from rec_to_nwb.processing.time.continuous_time_extractor import ContinuousTimeExtractor
from rec_to_nwb.processing.time.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class FlAnalogExtractor:

    @staticmethod
    def extract_analog_for_single_dataset(analog_files, continuous_time_file):
        single_dataset_data = {}
        for analog_file in analog_files:
            if not 'timestamps' in analog_file:
                analog_data = readTrodesExtractedDataFile(analog_files[analog_file])
                values = analog_data['data']
                single_dataset_data[analog_data['id']] = values
            else:
                continuous_time_dict = ContinuousTimeExtractor.get_continuous_time_dict_file(continuous_time_file)
                timestamp = readTrodesExtractedDataFile(analog_files[analog_file])
                keys = [key[0] for key in timestamp['data']]
                single_dataset_data[analog_file] = TimestampConverter.convert_timestamps(continuous_time_dict, keys)
        return single_dataset_data




