from rec_to_nwb.processing.nwb.components.position.fl_position_builder import FlPositionBuilder
from rec_to_nwb.processing.nwb.components.position.fl_position_extractor import FlPositionExtractor


class FlPositionManager:
    def __init__(self, datasets, conversion):
        self.fl_position_extractor = FlPositionExtractor(datasets)
        self.fl_position_builder = FlPositionBuilder()
        self.conversion = conversion

    def get_fl_position(self):
        position_data = self.fl_position_extractor.get_position()
        timestamps = self.fl_position_extractor.get_timestamps()
        return self.fl_position_builder.build(position_data, timestamps, self.conversion)
