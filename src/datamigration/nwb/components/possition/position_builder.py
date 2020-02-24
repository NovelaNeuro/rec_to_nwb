from src.datamigration.nwb.components.possition.position_creator import PositionCreator
from src.datamigration.nwb.components.possition.position_extractor import PositionExtractor


class PositionBuilder:
    def __init__(self, datasets, continuous_time_dicts):
        self.position_extractor = PositionExtractor(datasets, continuous_time_dicts)
        self.position_creator = PositionCreator()

    def build(self):
        position_data = self.position_extractor.get_position()
        timestamps = self.position_extractor.get_timestamps()
        return self.position_creator.create_position(position_data, timestamps)
