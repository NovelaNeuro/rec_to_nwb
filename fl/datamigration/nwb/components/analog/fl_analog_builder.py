import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class AnalogBuilder:

    def __init__(self, fl_analog):
        self.analog_data = fl_analog.data
        self.timestamps = fl_analog.timestamps

    def build(self):
        behavioral_events = self.__create_behavioral_events()
        behavioral_events.add_timeseries(
            self.__build_timeseries(
                name='Analog',
                data=self.analog_data,
                timestamps=self.timestamps))

        return behavioral_events

    @classmethod
    def __create_behavioral_events(cls):
        return BehavioralEvents(name="analog")

    def __build_timeseries(self, name, data, timestamps):
        return TimeSeries(name=name,
                          description='-',
                          data=data,
                          timestamps=timestamps)
