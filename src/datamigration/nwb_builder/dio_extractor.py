import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class DioExtractor:

    def __init__(self, dio_path):
        self.dio_path = dio_path

    def get_dio(self):
        behavioral_timestamps_in = []
        behavioral_timeseries_in = []
        behavioral_timestamps_out = []
        behavioral_timeseries_out = []
        for filename in os.listdir(self.dio_path):
            if filename.endswith(".dat"):
                dio_data = readTrodesExtractedDataFile(self.dio_path + '/' + filename)
                if 'Din' in filename:
                    for recorded_event in dio_data['data']:
                        behavioral_timestamps_in.append(recorded_event[0])
                        behavioral_timeseries_in.append(recorded_event[1])
                else:
                    for recorded_event in dio_data['data']:
                        behavioral_timestamps_out.append(recorded_event[0])
                        behavioral_timeseries_out.append(recorded_event[1])

        return BehavioralEvents(name='behavioral name',
                                time_series=[
                                             TimeSeries(name='behavioral timeseries in',
                                                        data=behavioral_timeseries_in,
                                                        timestamps=behavioral_timestamps_in),
                                             TimeSeries(name='behavioral timeseries out',
                                                        data=behavioral_timeseries_out,
                                                        timestamps=behavioral_timestamps_out)
                                             ]
                                )
