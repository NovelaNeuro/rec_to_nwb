from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.creators.dio_creator import DioCreator
from src.datamigration.nwb_builder.extractors.dio_extractor import DioManager


class DioInjector:
    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.metadata = metadata

    def build(self, nwb_content):
        dio_creator = DioCreator()
        dio_extractor = DioManager(datasets=self.datasets, metadata=self.metadata)
        extracted_dio = dio_extractor.get_dio()
        behavioral_event = BehavioralEvents(name='list of processed DIO`s', )
        dio_time_series = dio_creator.create_dio_time_series(behavioral_event, extracted_dio)
        nwb_content.processing["behavior"].add_data_interface(dio_time_series)
