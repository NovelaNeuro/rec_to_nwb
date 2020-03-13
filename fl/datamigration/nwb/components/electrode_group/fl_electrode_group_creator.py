from ndx_fllab_novela.fl_electrode_group import FLElectrodeGroup

from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeGroupCreator:

    @classmethod
    def create(cls, fl_fl_electrode_group):
        validate_parameters_not_none(__name__, fl_fl_electrode_group)
        validate_parameters_not_none(__name__, fl_fl_electrode_group.metadata, fl_fl_electrode_group.device)

        return FLElectrodeGroup(
            id=fl_fl_electrode_group.metadata['id'],
            device=fl_fl_electrode_group.device,
            location=str(fl_fl_electrode_group.metadata['location']),
            description=str(fl_fl_electrode_group.metadata['description']),
            name='electrode group ' + str(fl_fl_electrode_group.metadata["id"])
        )