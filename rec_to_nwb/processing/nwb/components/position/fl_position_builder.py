from rec_to_nwb.processing.nwb.components.position.fl_position import \
    FlPosition


class FlPositionBuilder:

    @staticmethod
    def build(position_data, column_labels, timestamps, conversion):
        return FlPosition(position_data, column_labels, timestamps, conversion)
