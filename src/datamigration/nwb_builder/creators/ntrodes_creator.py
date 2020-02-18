from ndx_franklab_novela.ntrode import NTrode


class NTrodesCreator:

    @staticmethod
    def create_ntrode(metadata, device, map_list):
        return NTrode(
            probe_id=metadata["probe_id"],
            ntrode_id=metadata['ntrode_id'],
            device=device,
            location='-',
            description='-',
            name='ntrode ' + str(metadata['ntrode_id']),
            map=map_list
        )