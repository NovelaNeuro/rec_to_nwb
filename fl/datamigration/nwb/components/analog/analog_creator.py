import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class AnalogCreator:

    @classmethod
    def create(cls, fl_analog):
        behavioral_events = AnalogCreator.__create_behavioral_events()
        behavioral_events.add_timeseries(
            AnalogCreator.__build_timeseries(
                name='Analog',
                data=fl_analog.data,
                timestamps=fl_analog.timestamps))

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
