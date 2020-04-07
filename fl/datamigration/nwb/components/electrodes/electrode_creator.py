from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class ElectrodesCreator:

    def __init__(self):
        self.electrode_id = -1

    def create(self, nwb_content, fl_electrode):
        self.__validate_parameters(fl_electrode, nwb_content)
        self.electrode_id += 1

        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=fl_electrode.electrode_group,
            id=self.electrode_id
        )

    @staticmethod
    def __validate_parameters(fl_electrode, nwb_content):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(nwb_content))
        validation_registrator.register(NotNoneValidator(fl_electrode))
        validation_registrator.validate()

        electrode_group_validation_registrator = ValidationRegistrator()
        electrode_group_validation_registrator.register(NotNoneValidator(fl_electrode.electrode_group))
        electrode_group_validation_registrator.validate()

