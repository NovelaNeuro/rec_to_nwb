from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.creators.dio_creator import DioCreator
from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor


class DioBuilder():
    def __init__(self, nwb_content, datasets, metadata):
        dio_creator = DioCreator()
        dio_extractor = DioExtractor(datasets=datasets, metadata=metadata)
        extracted_dio = dio_extractor.get_dio()
        behavioral_event = BehavioralEvents(name='list of processed DIO`s', )
        dio_time_series = dio_creator.create_dio_time_series(behavioral_event, extracted_dio)
        nwb_content.processing["behavior"].add_data_interface(dio_time_series)
