from fl.datamigration.nwb.components.position.fl_position_builder import LfPositionBuilder
from fl.datamigration.nwb.components.position.position_creator import PositionCreator
from fl.datamigration.nwb.components.position.fl_position_extractor import LfPositionExtractor


class LfPositionManager:
    def __init__(self, datasets):
        self.fl_position_extractor = LfPositionExtractor(datasets)
        self.fl_position_builder = LfPositionBuilder()

    def get_fl_position(self):
        position_data = self.fl_position_extractor.get_position()
        timestamps = self.fl_position_extractor.get_timestamps()
        return self.fl_position_builder.build(position_data, timestamps)

