from fldatamigration.processing.nwb.components.position.fl_position_builder import FlPositionBuilder
from fldatamigration.processing.nwb.components.position.position_creator import PositionCreator
from fldatamigration.processing.nwb.components.position.fl_position_extractor import FlPositionExtractor


class FlPositionManager:
    def __init__(self, datasets):
        self.fl_position_extractor = FlPositionExtractor(datasets)
        self.fl_position_builder = FlPositionBuilder()

    def get_fl_position(self):
        position_data = self.fl_position_extractor.get_position()
        timestamps = self.fl_position_extractor.get_timestamps()
        return self.fl_position_builder.build(position_data, timestamps)

