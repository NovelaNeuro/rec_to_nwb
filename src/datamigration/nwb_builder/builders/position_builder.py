import logging.config
import os

from src.datamigration.nwb_builder.creators.position_creator import PositionCreator
from src.datamigration.nwb_builder.extractors.position_extractor import PositionExtractor

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class PositionBuilder:
    def __init__(self, datasets):
        self.position_extractor = PositionExtractor(datasets)
        self.position_creator = PositionCreator()

    def build(self):
        position_data = self.position_extractor.get_position()
        timestamps = self.position_extractor.get_timestamps()
        return self.position_creator.create_position(position_data, timestamps)

