import logging.config
import os

from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.builders.dio_builder import DioBuilder
from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_files import DioFiles
from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioManager:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.dio_directories = datasets
        self.all_dio_timeseries = metadata['behavioral_events']
        self.dio_manager = DioFiles()
        self.continuous_time_extractor = ContinuousTimeExtractor()
        self.timestamp_converter = TimestampConverter()
        self.dio_builder = DioBuilder()

    def get_dio(self):
        for dataset in self.datasets:
            dict_dataset = self.continuous_time_extractor.get_continuous_time_dict_file(dataset.get_continuous_time())
            self.dio_builder.build_for_single_dataset(dataset=dataset, continuous_time_dict=dict_dataset,
                                                      all_dio_timeseries=self.all_dio_timeseries)
        return self.all_dio_timeseries
