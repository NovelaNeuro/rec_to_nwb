from ndx_fllab_novela.ntrode import NTrode


class NTrodesCreator:

    @staticmethod
    def create_ntrode(lf_ntrodes):
        return NTrode(
            probe_id=lf_ntrodes.metadata["probe_id"],
            ntrode_id=lf_ntrodes.metadata['ntrode_id'],
            device=lf_ntrodes.device,
            location='-',
            description='-',
            map=lf_ntrodes.map_list,
            name='ntrode ' + str(lf_ntrodes.metadata['ntrode_id']),
        )