from fl.processing.nwb.components.position.fl_position import FlPosition


class FlPositionBuilder:

    @staticmethod
    def build(position_data, timestamps):
        return FlPosition(position_data, timestamps)
