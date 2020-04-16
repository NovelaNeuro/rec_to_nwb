from fl.datamigration.tools.validate_parameters import validate_parameters_not_none

from ndx_fllab_novela.nwb_electrode_group import NwbElectrodeGroup

class ElectrodeGroupFactory:

    @classmethod
    def create_electrode_group(cls, fl_nwb_electrode_group):
        validate_parameters_not_none(__name__, fl_nwb_electrode_group)
        validate_parameters_not_none(__name__, fl_nwb_electrode_group.metadata, fl_nwb_electrode_group.device)

        return NwbElectrodeGroup(
            id=fl_nwb_electrode_group.metadata['id'],
            device=fl_nwb_electrode_group.device,
            location=str(fl_nwb_electrode_group.metadata['location']),
            description=str(fl_nwb_electrode_group.metadata['description']),
            name='electrode group ' + str(fl_nwb_electrode_group.metadata["id"])
        )