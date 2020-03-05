from pynwb.behavior import Position

from fl.datamigration.tools.validate_input_parameters import validate_input_parameters


class PositionCreator:

    @staticmethod
    def create(lf_position):
        validate_input_parameters(__name__, lf_position)
        validate_input_parameters(__name__, lf_position.position_data, lf_position.timestamps)

        position = Position()
        position.create_spatial_series(
            name='series',
            data=lf_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=lf_position.timestamps
        )
        return position
