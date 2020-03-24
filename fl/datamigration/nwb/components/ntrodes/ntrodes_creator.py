from ndx_fllab_novela.ntrode import NTrode


class NTrodesCreator:

    @staticmethod
    def create_ntrode(fl_ntrodes):
        return NTrode(
            probe_id=fl_ntrodes.metadata["probe_id"],
            ntrode_id=fl_ntrodes.metadata['ntrode_id'],
            bad_channels=fl_ntrodes.metadata['bad_channels'],
            device=fl_ntrodes.device,
            location='-',
            description='-',
            map=fl_ntrodes.map_list,
            name='ntrode ' + str(fl_ntrodes.metadata['ntrode_id']),
        )