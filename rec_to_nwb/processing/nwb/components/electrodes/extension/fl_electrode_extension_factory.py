from rec_to_nwb.processing.tools.filter_probe_by_type import filter_probe_by_type
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeExtensionFactory:

    @classmethod
    def create_rel(cls, probes_metadata, electrode_groups_metadata):
        validate_parameters_not_none(__name__, probes_metadata, electrode_groups_metadata)

        rel_x, rel_y, rel_z = [], [], []
        for electrode_group_metadata in electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for electrode in shank['electrodes']:
                    rel_x.append(float(electrode['rel_x']))
                    rel_y.append(float(electrode['rel_y']))
                    rel_z.append(float(electrode['rel_z']))
        return {'rel_x': rel_x, 'rel_y': rel_y, 'rel_z': rel_z}

    @classmethod
    def create_ntrode_id(cls, ntrode_metadata):
        validate_parameters_not_none(__name__, ntrode_metadata)

        ntrode_id = []
        [ntrode_id.extend([ntrode['ntrode_id']] * len(ntrode['map'])) for ntrode in ntrode_metadata]
        return ntrode_id

    @classmethod
    def create_channel_id(cls, ntrode_metadata):
        validate_parameters_not_none(__name__, ntrode_metadata)

        channel_id = []
        for ntrode in ntrode_metadata:
            [channel_id.append(map_index) for map_index in ntrode['map']]
        return channel_id

    @classmethod
    def create_bad_channels(cls, ntrode_metadata):
        validate_parameters_not_none(__name__, ntrode_metadata)

        bad_channels = []
        for ntrode in ntrode_metadata:
            bad_channels.extend(
                [bool(counter in ntrode['bad_channels']) for counter, _ in enumerate(ntrode['map'])]
            )
        return bad_channels

    @classmethod
    def create_hw_chan(cls, spike_n_trodes):
        validate_parameters_not_none(__name__, spike_n_trodes)

        hw_chan = []
        for spike_n_trode in spike_n_trodes:
            [hw_chan.append(int(spike_channel.hw_chan)) for spike_channel in spike_n_trode.spike_channels]
        return hw_chan

    @classmethod
    def create_probe_shank(cls, probes_metadata, electrode_groups_metadata):
        validate_parameters_not_none(__name__, probes_metadata, electrode_groups_metadata)

        probe_shank = []
        for electrode_group_metadata in electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group_metadata['device_type'])
            [probe_shank.extend([shank['shank_id']] * len(shank['electrodes'])) for shank in probe_metadata['shanks']]
        return probe_shank

    @classmethod
    def create_probe_electrode(cls, probes_metadata, electrode_groups_metadata):
        validate_parameters_not_none(__name__, probes_metadata)

        probe_electrode = []
        for electrode_group_metadata in electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group_metadata['device_type'])
            for shank in probe_metadata['shanks']:
                [probe_electrode.append(electrode['id']) for electrode in shank['electrodes']]
        return probe_electrode

