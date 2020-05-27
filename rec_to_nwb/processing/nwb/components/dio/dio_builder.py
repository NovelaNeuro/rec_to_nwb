import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

path = os.path.dirname(os.path.abspath(__file__))


class DioBuilder:

    def __init__(self, data, dio_metadata, unit):
        self.dio_metadata = dio_metadata
        self.data = data
        self.unit = unit

    def build(self):
        behavioral_events = self.__create_behavioral_events()
        for dio_event in self.dio_metadata:
            behavioral_events.add_timeseries(
                self.__build_timeseries(
                    name=dio_event['name'],
                    description=dio_event['description'],
                    data=self.data[dio_event['description']],
                    unit=self.unit
                )
            )
        return behavioral_events

    @classmethod
    def __create_behavioral_events(cls):
        return BehavioralEvents(name="behavioral_events")

    @classmethod
    def __build_timeseries(cls, name, description, data, unit):
        return TimeSeries(name=name,
                          description=description,
                          data=data[1],
                          timestamps=data[0],
                          unit=unit
                          )
