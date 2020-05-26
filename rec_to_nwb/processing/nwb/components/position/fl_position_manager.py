from rec_to_nwb.processing.nwb.components.position.fl_position_builder import FlPositionBuilder
from rec_to_nwb.processing.nwb.components.position.fl_position_extractor import FlPositionExtractor


class FlPositionManager:
    def __init__(self, datasets, conversion):
        self.conversion = conversion
        self.fl_position_extractor = FlPositionExtractor(datasets)
        self.fl_position_builder = FlPositionBuilder()

    def get_fl_position(self):
        position_data = self.fl_position_extractor.get_position()
        column_labels = self.fl_position_extractor.get_column_labels()
        timestamps = self.fl_position_extractor.get_timestamps()
        return self.fl_position_builder.build(position_data, column_labels, timestamps, self.conversion)
