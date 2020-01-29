from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup


class ElectrodeGroupBuilder:

    @staticmethod
    def create_electrode_group(metadata, device):
        return FLElectrodeGroup(
            id=metadata['id'],
            device=device,
            location=str(metadata['location']),
            description=str(metadata['description']),
            name='electrode group ' + str(metadata["id"])
        )