import logging.config
import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ContinuousTimeExtractor:

    @staticmethod
    def get_continuous_time_dict(files):
        return [ContinuousTimeExtractor.get_continuous_time_dict_file(file) for file in files]

    @staticmethod
    def get_continuous_time_dict_file(file):
        logger.info('Reading continuous time dict from: ' + str(file))
        continuous_time = readTrodesExtractedDataFile(file)
        return {str(data[0]): float(data[1]) for data in continuous_time['data']}

