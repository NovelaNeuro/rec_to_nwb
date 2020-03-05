from fl.datamigration.nwb.components.position.fl_position import LfPosition


class LfPositionBuilder:

    @staticmethod
    def build(position_data, timestamps):
        return LfPosition(position_data, timestamps)
