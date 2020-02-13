import logging.config
import os

import numpy as np
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioExtractor:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.dio_directories = datasets
        self.all_dio_timeseries = metadata['behavioral_events']
        self.add_fields_to_dio(all_dio_timeseries=self.all_dio_timeseries)
        self.behavioral_event = BehavioralEvents(name='list of processed DIO`s', )
        self.dio_manager = DioManager(metadata=metadata)
        self.continuous_time_extractor = ContinuousTimeExtractor()

    def get_dio(self):
        for dataset in self.datasets:
            self.create_timeseries(dataset=dataset,
                                   continuous_time_dict=self.continuous_time_extractor.get_continuous_time_dict_dataset(
                                       dataset=dataset))
        return self.all_dio_timeseries

    @staticmethod
    def add_fields_to_dio(all_dio_timeseries):
        for series in all_dio_timeseries:
            series["dio_timeseries"] = []
            series["dio_timestamps"] = []

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
                    self.create_timeseries_for_single_event(dio_time_series, recorded_event, continuous_time_dict)
            except TypeError:
                message = 'there is no data for event ' + str(dio_time_series['name'])
                logger.exception(message)

    # ToDo this should be in Creator!!!
    @staticmethod
    def create_timeseries_for_single_event(time_series, event, continuous_time_dict):
        time_series["dio_timeseries"].append(event[1])
        key = str(event[0])
        value = continuous_time_dict.get([key], float('nan')) / 1E9
        if np.isnan(value):
            message = 'Following key: ' + str(key) + ' does not exist in continioustime dictionary!'
            logger.exception(message)
        time_series["dio_timestamps"].append(value)
        return time_series
