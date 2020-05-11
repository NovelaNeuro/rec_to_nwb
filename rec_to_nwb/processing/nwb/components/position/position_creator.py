from pynwb.behavior import Position

from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class PositionCreator:

    @staticmethod
    def create(fl_position):
        validate_parameters_not_none(__name__, fl_position)
        validate_parameters_not_none(__name__, fl_position.position_data, fl_position.timestamps)

        position = Position()
        position.create_spatial_series(
            name='series',
            data=fl_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position
