from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from fl.datamigration.validation.not_none_validator import NotNoneValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator


class FlElectrodeGroupManager:

    def __init__(self, electrode_groups_metadata):
        self.electrode_groups_metadata = electrode_groups_metadata

    def get_fl_nwb_electrode_groups(self, probes):
        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotNoneValidator(self.electrode_groups_metadata))
        validation_registrator.register(NotNoneValidator(probes))
        validation_registrator.validate()

        return [FlNwbElectrodeGroup(
            metadata=electrode_group_metadata,
            device=probes[counter]
        ) for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata)]
