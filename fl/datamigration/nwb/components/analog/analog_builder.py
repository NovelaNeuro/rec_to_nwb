import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class DioBuilder:

    def __init__(self, analog_data):



    def build(self):
        behavioral_events = self.__create_behavioral_events()

        return behavioral_events

    @classmethod
    def __create_behavioral_events(cls):
        return BehavioralEvents(name="analog")

    def __build_timeseries(self):
        return TimeSeries(name=name,
                          description=description,
                          data=self.values,
                          timestamps=self.timestamps)
