from pynwb.behavior import Position

from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class PositionCreator:

    @staticmethod
    def create(fl_position):
        validate_parameters_not_none(
            class_name=__name__,
            args=[fl_position],
            args_name=[NameExtractor.extract_name(PositionCreator.create)[0]]
        )
        validate_parameters_not_none(
            class_name=__name__,
            args=[fl_position.position_data, fl_position.timestamps],
            args_name=[NameExtractor.extract_name(fl_position.__init__)[1],
                       NameExtractor.extract_name(fl_position.__init__)[2]]
        )

        position = Position()
        position.create_spatial_series(
            name='series',
            data=fl_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position
