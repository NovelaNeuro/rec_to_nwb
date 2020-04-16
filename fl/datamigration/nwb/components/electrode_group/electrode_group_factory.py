from pynwb.ecephys import ElectrodeGroup

from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodeGroupFactory:

    @classmethod
    def create_electrode_group(cls, fl_electrode_group):
        validate_parameters_not_none(__name__, fl_electrode_group)
        validate_parameters_not_none(__name__, fl_electrode_group.metadata, fl_electrode_group.device)

        return ElectrodeGroup(
            device=fl_electrode_group.device,
            location=str(fl_electrode_group.metadata['location']),
            description=str(fl_electrode_group.metadata['description']),
            name='electrode group ' + str(fl_electrode_group.metadata["id"])
        )