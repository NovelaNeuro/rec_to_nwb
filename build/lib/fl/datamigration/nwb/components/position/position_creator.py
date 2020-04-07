from pynwb.behavior import Position

from fl.datamigration.tools.validate_input_parameters import validate_input_parameters


class PositionCreator:

    @staticmethod
    def create(fl_position):
        validate_input_parameters(__name__, fl_position)
        validate_input_parameters(__name__, fl_position.position_data, fl_position.timestamps)

        position = Position()
        position.create_spatial_series(
            name='series',
            data=fl_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position
