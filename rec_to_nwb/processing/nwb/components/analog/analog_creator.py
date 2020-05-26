import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class AnalogCreator:

    @classmethod
    def create(cls, fl_analog, unit):
        behavioral_events = AnalogCreator.__create_behavioral_events()
        behavioral_events.add_timeseries(
            AnalogCreator.__build_timeseries(
                name='analog',
                data=fl_analog.data,
                timestamps=fl_analog.timestamps,
                unit=unit
            )
        )

        return behavioral_events

    @staticmethod
    def __create_behavioral_events():
        return BehavioralEvents(name="analog")

    @staticmethod
    def __build_timeseries(name, data, timestamps, unit):
        return TimeSeries(name=name,
                          description='-',
                          data=data,
                          timestamps=timestamps,
                          unit=unit
                          )
