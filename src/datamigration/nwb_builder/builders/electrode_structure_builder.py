from src.datamigration.nwb_builder.builders.device_creator import DeviceCreator
from src.datamigration.nwb_builder.builders.device_injector import DeviceInjector
from src.datamigration.nwb_builder.builders.electrodes_builder import ElectrodesBuilder
from src.datamigration.nwb_builder.creators.electrode_group_creator import ElectrodeGroupBuilder
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.nwb_builder_tools.electrode_addentum import ElectrodeAddendum


class ElectrodeStructureBuilder:
    def __init__(self):



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
        probe_metadata = ProbeManager().get_probe(electrode_group_metadata['device_type'])

        device = DeviceCreator().create_device(probe_metadata, device_counter)
        device_counter += 1
        DeviceInjector(nwb_content).join_device(device)

        electrode_group = ElectrodeGroupBuilder().create_electrode_group(electrode_group_metadata, device)
        ElectrodeGroupInjector(nwb_content).join_electrode_group(electrode_group)

        ElectrodesBuilder()

        create_electrodes(probes,
                          nwb_content,
                          electrode_group,
                          device_type=electrode_group_metadata['device_type'],
                          electrode_addendum=electrode_addendum)

    add_extensions_to_electrodes(header, nwb_content, electrode_addendum)



def create_electrodes(probes, nwb_content, electrode_group, device_type, electrode_addendum):
    for probe_metadata in probes:
        if probe_metadata['probe_type'] == device_type:

            for shank in probe_metadata['shanks']:
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
