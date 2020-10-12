import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class OldFlAnalogExtractor:

    @staticmethod
    def extract_analog_for_single_dataset(analog_files):
        single_dataset_data = {}
        for analog_file in analog_files:
            analog_data = readTrodesExtractedDataFile(analog_files[analog_file])
            values = analog_data['data']
            single_dataset_data[analog_data['id']] = values
        return single_dataset_data
