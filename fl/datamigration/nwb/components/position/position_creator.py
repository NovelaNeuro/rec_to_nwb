from pynwb.behavior import Position

from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class PositionCreator:

    @staticmethod
    def create(fl_position):
        validator_registrator = ValidationRegistrator()
        validator_registrator.register(NotNoneValidator(fl_position))
        validator_registrator.register(NotNoneValidator(fl_position.position_data))
        validator_registrator.register(NotNoneValidator(fl_position.timestamps))
        validator_registrator.validate()
        position = Position()
        position.create_spatial_series(
            name='series',
            data=fl_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position
