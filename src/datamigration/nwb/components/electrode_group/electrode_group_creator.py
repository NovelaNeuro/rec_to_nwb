from ndx_franklab_novela.fl_electrode_group import FLElectrodeGroup


class ElectrodeGroupCreator:

    @classmethod
    def create_electrode_group(cls,metadata, device):
        return FLElectrodeGroup(
            id=metadata['id'],
            device=device,
            location=str(metadata['location']),
            description=str(metadata['description']),
            name='electrode group ' + str(metadata["id"])
        )