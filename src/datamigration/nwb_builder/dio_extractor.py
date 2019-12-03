import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class DioExtractor:

    def __init__(self, dio_path):
        self.dio_path = dio_path

    def get_dio(self):
        behavioral_timestamps = []
        behavioral_timeseries = []
        for filename in os.listdir(self.dio_path):
            if filename.endswith(".dat"):
                dio_data = readTrodesExtractedDataFile(self.dio_path + '/' + filename)
                for recorded_event in dio_data['data']:
                    behavioral_timestamps.append(recorded_event[0])
                    behavioral_timeseries.append(recorded_event[1])

        return BehavioralEvents(name='behavioral name',
                                time_series=TimeSeries(name='behavioral timeseries',
                                                       data=behavioral_timeseries,
                                                       timestamps=behavioral_timestamps))