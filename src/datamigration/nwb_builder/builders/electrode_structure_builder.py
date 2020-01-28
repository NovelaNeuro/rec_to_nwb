from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.probe import Probe
from src.datamigration.nwb_builder.nwb_builder_tools.electrode_addentum import ElectrodeAddendum


def build_electrode_structure(header, metadata, nwb_content, probes):
    """
        For each electrode group in metadata.yml, check if device exist.
        If not create one.
        Create electrode_group
        Create electrodes from corresponding probe_type in probe.yml
    """

    device_counter = 0
    electrode_addendum = ElectrodeAddendum()

    for electrode_group_metadata in metadata['electrode groups']:
        device = check_device(probes, nwb_content, electrode_group_metadata['device_type'], device_counter)
        electrode_group = create_electrode_group(nwb_content, electrode_group_metadata, device)
        create_electrodes(probes,
                          nwb_content,
                          electrode_group,
                          device_type=electrode_group_metadata['device_type'],
                          electrode_addendum=electrode_addendum)

    add_extensions_to_electrodes(header, nwb_content, electrode_addendum)


def check_device(probes, nwb_content, device_type, device_counter):
    for device_name in nwb_content.devices:
        device = nwb_content.get_device(device_name)
        if device.probe_type == device_type:
            return device
    return create_device(probes, nwb_content, device_type, device_counter)


def create_device(probes, nwb_content, device_type, device_counter):
    probe = None
    for fl_probe in probes:
        if fl_probe['probe_type'] == device_type:
            probe = Probe(
                probe_type=fl_probe["probe_type"],
                contact_size=fl_probe["contact_size"],
                num_shanks=fl_probe['num_shanks'],
                id=device_counter,
                name=str(device_counter)
            )
    nwb_content.add_device(probe)
    device_counter += 1

    return probe


def create_electrode_group(nwb_content, metadata, device):
    electrode_group = FLElectrodeGroup(
        id=metadata['id'],
        device=device,
        location=str(metadata['location']),
        description=str(metadata['description']),
        name='electrode group ' + str(metadata["id"])
    )
    nwb_content.add_electrode_group(electrode_group)
    return electrode_group


def create_electrodes(probes, nwb_content, electrode_group, device_type, electrode_addendum):
    for fl_probe in probes:
        if fl_probe['probe_type'] == device_type:

            for shank in fl_probe['shanks']:
                for electrode in shank['electrodes']:
                    nwb_content.add_electrode(
                        x=0.0,
                        y=0.0,
                        z=0.0,
                        imp=1.0,
                        location='None',
                        filtering='None',
                        group=electrode_group,
                        id=electrode_addendum.electrode_counter)
                    electrode_addendum.rel_x.append(electrode['rel_x'])
                    electrode_addendum.rel_y.append(electrode['rel_y'])
                    electrode_addendum.rel_z.append(electrode['rel_z'])
                    electrode_addendum.electrode_counter += 1


def add_extensions_to_electrodes(header, nwb_content, electrode_addendum):
    spike_channels_list = []
    hw_chan = []
    for spike_n_trode in header.configuration.spike_configuration.spike_n_trodes:
        for spike_channel in spike_n_trode.spike_channels:
            spike_channels_list.append(spike_channel)

    for spike_channel, electrode in zip(spike_channels_list, nwb_content.electrodes):
        hw_chan.append(spike_channel.hw_chan)

    nwb_content.electrodes.add_column(
        name='hwChan',
        description='None',
        data=hw_chan
    )

    nwb_content.electrodes.add_column(
        name='rel_x',
        description='None',
        data=electrode_addendum.rel_x
    )

    nwb_content.electrodes.add_column(
        name='rel_y',
        description='None',
        data=electrode_addendum.rel_y
    )

    nwb_content.electrodes.add_column(
        name='rel_z',
        description='None',
        data=electrode_addendum.rel_z
    )
