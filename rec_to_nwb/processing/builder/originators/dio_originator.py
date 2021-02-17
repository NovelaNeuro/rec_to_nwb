import logging.config
import os

from rec_to_nwb.processing.nwb.components.dio.dio_builder import DioBuilder
from rec_to_nwb.processing.nwb.components.dio.dio_files import DioFiles
from rec_to_nwb.processing.nwb.components.dio.dio_injector import DioInjector
from rec_to_nwb.processing.nwb.components.dio.dio_manager import DioManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioOriginator:

    def __init__(self, metadata, datasets, convert_timestamps=True):
        self.metadata = metadata
        self.datasets = datasets
        self.convert_timestamps = convert_timestamps

    def make(self, nwb_content):
        logger.info('DIO: Prepare directories')
        dio_directories = [single_dataset.get_data_path_from_dataset('DIO') for single_dataset in self.datasets]
        logger.info('DIO: Prepare files')
        dio_files = DioFiles(dio_directories, self.metadata['behavioral_events'])
        logger.info('DIO: Retrieve data')
        dio_manager = DioManager(
            dio_files=dio_files.get_files(),
            dio_metadata=self.metadata['behavioral_events'],
            continuous_time_files=self.__get_continuous_time_files(),
            convert_timestamps=self.convert_timestamps
        )
        dio_data = dio_manager.get_dio()
        logger.info('DIO: Building')
        dio_builder = DioBuilder(
            dio_data,
            self.metadata['behavioral_events'],
            self.metadata['units']['behavioral_events']
        )
        behavioral_events = dio_builder.build()
        logger.info('DIO: Injecting into NWB')
        dio_injector = DioInjector(nwb_content)
        dio_injector.inject(behavioral_events, 'behavior')

    def __get_continuous_time_files(self):
        return [single_dataset.get_continuous_time() for single_dataset in self.datasets]
