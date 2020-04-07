from ndx_fllab_novela.nwb_electrode_group import NwbElectrodeGroup

from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class ElectrodeGroupFactory:

    @classmethod
    def create_nwb_electrode_group(cls, fl_nwb_electrode_group):
        cls.__validate_fl_nwb_electrode_group(fl_nwb_electrode_group)

        return NwbElectrodeGroup(
            id=fl_nwb_electrode_group.metadata['id'],
            device=fl_nwb_electrode_group.device,
            location=str(fl_nwb_electrode_group.metadata['location']),
            description=str(fl_nwb_electrode_group.metadata['description']),
            name='electrode group ' + str(fl_nwb_electrode_group.metadata["id"])
        )

    @staticmethod
    def __validate_fl_nwb_electrode_group(fl_nwb_electrode_group):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(fl_nwb_electrode_group))
        validation_registrator.validate()

        electrode_group_fields_validation_registrator = ValidationRegistrator()
        electrode_group_fields_validation_registrator.register(NotNoneValidator(fl_nwb_electrode_group.metadata))
        electrode_group_fields_validation_registrator.register(NotNoneValidator(fl_nwb_electrode_group.device))
        electrode_group_fields_validation_registrator.validate()