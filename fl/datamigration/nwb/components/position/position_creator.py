from pynwb.behavior import Position

from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class PositionCreator:

    @staticmethod
    def create(fl_position):
        PositionCreator.__validate([fl_position])
        PositionCreator.__validate([fl_position.position_data, fl_position.timestamps])
        position = Position()
        position.create_spatial_series(
            name='series',
            data=fl_position.position_data,
            reference_frame='Description defining what the zero-position is',
            timestamps=fl_position.timestamps
        )
        return position

    @staticmethod
    def __validate(parameters):
        validator_registrator = ValidationRegistrator()
        for parameter in parameters:
            validator_registrator.register(NotNoneValidator(parameter))
        validator_registrator.validate()
