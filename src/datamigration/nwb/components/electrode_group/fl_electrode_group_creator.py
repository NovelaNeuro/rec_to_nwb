from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup


class FlElectrodeGroupCreator:

    @classmethod
    def create(cls, lf_fl_electrode_group):
        return FLElectrodeGroup(
            id=lf_fl_electrode_group.metadata['id'],
            device=lf_fl_electrode_group.device,
            location=str(lf_fl_electrode_group.metadata['location']),
            description=str(lf_fl_electrode_group.metadata['description']),
            name='electrode group ' + str(lf_fl_electrode_group.metadata["id"])
        )