from src.datamigration.extension.ntrode import NTrode


class NTrodesCreator:

    def create_ntrode(self, metadata, device, map_list):
        ntrode = NTrode(
            probe_id=metadata["probe_id"],
            ntrode_id=metadata['ntrode_id'],
            device=device,
            location='-',
            description='-',
            name='ntrode ' + str(metadata['ntrode_id']),
            map=map_list
        )
        return ntrode