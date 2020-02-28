from src.datamigration.nwb.components.position.lf_position import LfPosition


class LfPositionBuilder:

    @staticmethod
    def build(position_data, timestamps):
        return LfPosition(position_data, timestamps)
