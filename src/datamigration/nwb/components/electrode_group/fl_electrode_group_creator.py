from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup

from src.datamigration.tools.validate_input_parameters import validate_input_parameters


class FlElectrodeGroupCreator:

    @classmethod
    def create(cls, lf_fl_electrode_group):
        validate_input_parameters(__name__, lf_fl_electrode_group)
        validate_input_parameters(__name__, lf_fl_electrode_group.metadata, lf_fl_electrode_group.device)

        return FLElectrodeGroup(
            id=lf_fl_electrode_group.metadata['id'],
            device=lf_fl_electrode_group.device,
            location=str(lf_fl_electrode_group.metadata['location']),
            description=str(lf_fl_electrode_group.metadata['description']),
            name='electrode group ' + str(lf_fl_electrode_group.metadata["id"])
        )