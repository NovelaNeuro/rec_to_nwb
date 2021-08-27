from pynwb.behavior import Position
from rec_to_nwb.processing.nwb.components.position.fl_position import \
    FlPosition
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import \
    validate_parameters_not_none


class PositionCreator:

    @beartype
    def create_all(self, fl_positions: list) -> Position:
        position = Position(name='position')
        for series_id, fl_position in enumerate(fl_positions):
            self.create(position, series_id, fl_position)
        return position

    @staticmethod
    @beartype
    def create(position: Position, series_id: int, fl_position: FlPosition):
        validate_parameters_not_none(__name__,
                                     fl_position.column_labels,
                                     fl_position.position_data,
                                     fl_position.conversion)
        position.create_spatial_series(
            name='series_' + str(series_id),
            description=fl_position.column_labels,
            data=fl_position.position_data,
            conversion=fl_position.conversion,
            reference_frame='Upper left corner of video frame',
            timestamps=fl_position.timestamps,
        )
