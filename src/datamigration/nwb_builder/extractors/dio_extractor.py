import os

from pynwb.base import TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.exceptions.missing_data_exception import MissingDataException


class DioExtractor:

    def __init__(self, data_path, metadata):
        self.data_path = data_path
        self.dio_paths = [dio_set for dio_set in os.listdir(data_path) if dio_set.endswith('DIO')]
        self.time_paths = [dio_set for dio_set in os.listdir(data_path) if dio_set.endswith('.time')]
        self.metadata = metadata

    def get_dio(self):  # todo refactor as this is too complex and is not unit tested
        behavioral_event = BehavioralEvents(name='list of processed DIO`s',)
        timestamps = {}
        timeseries = {}
        for i in range(len(self.dio_paths)):
            dio_set = self.dio_paths[i]
            time_set = self.time_paths[i]
            for dio_time_series in self.metadata['behavioral_events']:
                timestamps[dio_time_series['name']] = []
                timeseries[dio_time_series['name']] = []
            continuous_time_file = None
            for file in os.listdir(self.data_path + '/' + time_set):
                if file.endswith('continuoustime.dat'):
                    continuous_time_file = self.data_path + '/' + time_set + "/" + file
            if not continuous_time_file:
                raise MissingDataException("continuous time file not found")
            continuous_time = readTrodesExtractedDataFile(continuous_time_file)
            continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
            for dio_time_series in self.metadata['behavioral_events']:
                temp_timeseries = []
                temp_timestamps = []
                for dio_file in os.listdir(self.data_path + '/' + dio_set):
                    if dio_time_series['name'] + '.' in dio_file:
                        dio_data = readTrodesExtractedDataFile(self.data_path + '/' + dio_set + '/' + dio_file)
                        for recorded_event in dio_data['data']:
                            temp_timeseries.append(recorded_event[1])
                            key = str(recorded_event[0])
                            try:
                                value = continuous_time_dict[key]
                                temp_timestamps.append(float(value) / 1E9)
                            except KeyError:
                                temp_timestamps.append(float('nan'))
                timestamps[dio_time_series['name']].extend(temp_timestamps)
                timeseries[dio_time_series['name']].extend(temp_timeseries)
        for dio_time_series in self.metadata['behavioral_events']:
            behavioral_event.add_timeseries(time_series=TimeSeries(name=dio_time_series['name'],
                                                                   data=timeseries[dio_time_series['name']],
                                                                   timestamps=timestamps[dio_time_series['name']],
                                                                   description=dio_time_series['description'],
                                                                   )
                                            )

        return behavioral_event

