from rec_to_nwb.processing.nwb.components.position.fl_position import FlPosition


class FlPositionBuilder:

    @staticmethod
    def build(position_data, timestamps):
        return FlPosition(position_data, timestamps)
