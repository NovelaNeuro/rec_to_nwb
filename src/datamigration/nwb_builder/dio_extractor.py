import os

from pynwb.base import TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor


class DioExtractor:

    def __init__(self, data_path, metadata_path):
        self.data_path = data_path
        self.dio_paths = [dio_set for dio_set in os.listdir(data_path) if dio_set.endswith('DIO')]
        self.metadata = MetadataExtractor(metadata_path)

    def get_dio(self):
        behavioral_event = BehavioralEvents(name='',)
        for dio_time_series in self.metadata.behavioral_event:
            temp_timeseries = []
            temp_timestamps = []
            for dio_set in self.dio_paths:
                for dio_file in os.listdir(self.data_path + '/' + dio_set):
                    if dio_time_series['name'] in dio_file:
                        dio_data = readTrodesExtractedDataFile(self.data_path + '/' + dio_set + '/' + dio_file)
                        for recorded_event in dio_data['data']:
                            temp_timeseries.append(recorded_event[1])
                            temp_timestamps.append(recorded_event[0])
            behavioral_event.add_timeseries(time_series=TimeSeries(name=dio_time_series['name'],
                                                                   data=temp_timeseries,
                                                                   timestamps=temp_timestamps,
                                                                   description=dio_time_series['description'],
                                                                   )
                                            )
        return behavioral_event
