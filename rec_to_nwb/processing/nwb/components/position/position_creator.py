from pynwb.behavior import Position

from rec_to_nwb.processing.nwb.components.position.fl_position import FlPosition
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class PositionCreator:

    @staticmethod
    @beartype
    def create(fl_position: FlPosition) -> Position:
        validate_parameters_not_none(__name__, fl_position.column_labels, fl_position.position_data,
                                     fl_position.conversion, fl_position.timestamps)

        position = Position(name='position')
        position.create_spatial_series(
            name='series',
            description=fl_position.column_labels,
            data=fl_position.position_data,
            conversion=fl_position.conversion,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position
