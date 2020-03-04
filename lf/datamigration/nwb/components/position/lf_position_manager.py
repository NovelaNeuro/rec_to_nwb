from lf.datamigration.nwb.components.position.lf_position_builder import LfPositionBuilder
from lf.datamigration.nwb.components.position.position_creator import PositionCreator
from lf.datamigration.nwb.components.position.lf_position_extractor import LfPositionExtractor


class LfPositionManager:
    def __init__(self, datasets):
        self.lf_position_extractor = LfPositionExtractor(datasets)
        self.lf_position_builder = LfPositionBuilder()

    def get_lf_position(self):
        position_data = self.lf_position_extractor.get_position()
        timestamps = self.lf_position_extractor.get_timestamps()
        return self.lf_position_builder.build(position_data, timestamps)

