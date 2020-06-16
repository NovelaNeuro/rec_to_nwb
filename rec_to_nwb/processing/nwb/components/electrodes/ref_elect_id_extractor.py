from rec_to_nwb.processing.tools.beartype.beartype import beartype


class RefElectIdExtractor:

    @staticmethod
    @beartype
    def extract(spike_n_trodes: list, metadata: dict):
        ref_elect_id = []
        [
            ref_elect_id.extend(
                [metadata["ntrode probe channel map"][int(spike_n_trode.ref_n_trode_id)][int(spike_n_trode.ref_chan)]]
                * len(spike_n_trode.spike_channels)
            )
            for spike_n_trode in spike_n_trodes
        ]
