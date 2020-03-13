import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class AnalogCreator:

    def __init__(self, fl_analog):
        self.analog_data = fl_analog.data
        self.timestamps = fl_analog.timestamps

    def create(self):
        behavioral_events = AnalogCreator.__create_behavioral_events()
        behavioral_events.add_timeseries(
            AnalogCreator.__build_timeseries(
                name='Analog',
                data=self.analog_data,
                timestamps=self.timestamps))

        return behavioral_events

    @staticmethod
    def __create_behavioral_events():
        return BehavioralEvents(name="analog")

    @staticmethod
    def __build_timeseries(name, data, timestamps):
        return TimeSeries(name=name,
                          description='-',
                          data=data,
                          timestamps=timestamps)
