import os

from pynwb.base import TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.exceptions.missing_data_exception import MissingDataException


class DioExtractor:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.dio_directories = datasets
        self.metadata = metadata
        self.all_dio_timeseries = metadata['behavioral_events']

    def get_dio(self):
        behavioral_event = BehavioralEvents(name='list of processed DIO`s',)
        for i in range(len(self.dio_paths)):
            dio_set = self.dio_paths[i]
            time_set = self.time_paths[i]
            continuous_time_file = None
            for file in os.listdir(self.data_path + '/' + time_set):
                if file.endswith('continuoustime.dat'):
                    continuous_time_file = self.data_path + '/' + time_set + "/" + file
            if not continuous_time_file:
                raise MissingDataException("continuous time file not found")
            continuous_time = readTrodesExtractedDataFile(continuous_time_file)
            continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
            self.save_timeseries(behavioral_event)

    def create_timeseries(self, continuous_time_dict):
        for dio_time_series in self.all:
            for dio_file in os.listdir(self.data_path + '/' + dio_set):
                if dio_time_series['name'] + '.' in dio_file:
                    dio_data = readTrodesExtractedDataFile(self.data_path + '/' + dio_set + '/' + dio_file)
                    for recorded_event in dio_data['data']:
                        single_timeseries = self.create_timeseries_for_single_event(dio_time_series, recorded_event,
                                                                                    continuous_time_dict)

    def create_timeseries_for_single_event(self, time_series, event, continuous_time_dict):
        time_series["dio_timeseries"].append(event[1])
        key = str(event[0])
        try:
            value = continuous_time_dict[key]
            time_series["dio_timestamps"].append(float(value) / 1E9)
        except KeyError:
            time_series["dio_timestamps"].append(float('nan'))

    def save_timeseries(self, behavioral_event, all_time_series):
        for dio_time_series in self.all_time_series:
            behavioral_event.add_timeseries(time_series=TimeSeries(name=dio_time_series['name'],
                                                                   data=dio_time_series["dio_timeseries"],
                                                                   timestamps=dio_time_series["dio_timestamps"],
                                                                   description=dio_time_series['description'],
                                                                   )
                                            )

