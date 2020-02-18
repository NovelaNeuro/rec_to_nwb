import logging.config
import os

from pynwb import TimeSeries
from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DioBuilder:

    def __init__(self, directories, dio_metadata, continuous_time_dicts):
        self.directories = directories
        self.continuous_time_dicts = continuous_time_dicts
        self.dio_metadata = dio_metadata
        self.dio_manager = DioManager(directories=directories,
                                      dio_metadata=dio_metadata)
        self.dio_extractor = DioExtractor(filtered_dio_files=self.dio_manager.get_dio_files(),
                                          continuous_time_dicts=continuous_time_dicts)
        self.data = self.dio_extractor.get_dio()

    def build(self):
        behavioral_events = self.__create_behaviorl_events()
        for dio_event in self.dio_metadata:
            behavioral_events.add_timeseries(
                self.__build_timeseries(
                    name=dio_event['name'],
                    description=dio_event['description'],
                    data=self.data[dio_event['name']]))
        return behavioral_events

    @classmethod
    def __create_behaviorl_events(cls):
        return BehavioralEvents(name="behavioral_events")

    def __build_timeseries(self, name, description, data):
        return TimeSeries(name=name,
                          description=description,
                          data=[record[1] for record in data],
                          timestamps=[record[0] for record in data])
