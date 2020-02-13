import logging.config
import os

from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager
from src.datamigration.nwb_builder.nwb_builder_tools.timestamp_converter import TimestampConverter

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.dio_directories = datasets
        self.all_dio_timeseries = metadata['behavioral_events']
        self.behavioral_event = BehavioralEvents(name='list of processed DIO`s', )
        self.dio_manager = DioManager(metadata=metadata)
        self.continuous_time_extractor = ContinuousTimeExtractor()
        self.timestampConverter = TimestampConverter()


    def get_dio(self):
        for dataset in self.datasets:
            self.create_timeseries(dataset=dataset,
                                   continuous_time_dict=self.continuous_time_extractor.get_continuous_time_dict_dataset(
                                       dataset=dataset)
                                   )
        return self.all_dio_timeseries


    # ToDo This should be in Creator!!!
    def create_timeseries(self, continuous_time_dict, dataset):
        dio_dict = self.dio_manager.get_dio_dict(dataset.get_data_path_from_dataset('DIO'))
        for dio_time_series in self.all_dio_timeseries:
            try:
                dio_data = readTrodesExtractedDataFile(dataset.get_data_path_from_dataset('DIO') +
                                                       dio_dict[dio_time_series['name']])
            except KeyError:
                message = "there is no " + str(dio_time_series['name']) + " file"
                logger.exception(message)
            try:
                for recorded_event in dio_data['data']:
                    dio_time_series["dio_timeseries"].append(recorded_event[1])
                    dio_time_series["dio_timestamps"].append(recorded_event[0])

                convertedTimestamps = timestampConverter.convert_timestamps(continuous_time_dict, dio_time_series["dio_timestamps"])
                dio_time_series["dio_timestamps"] = convertedTimestamps
            except TypeError:
                message = 'there is no data for event ' + str(dio_time_series['name'])
                logger.exception(message)

