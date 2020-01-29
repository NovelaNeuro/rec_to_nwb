from src.datamigration.nwb_builder.builders.device_creator import DeviceCreator
from src.datamigration.nwb_builder.builders.device_injector import DeviceInjector
from src.datamigration.nwb_builder.builders.electrodes_builder import ElectrodesBuilder
from src.datamigration.nwb_builder.creators.electrode_group_creator import ElectrodeGroupBuilder
from src.datamigration.nwb_builder.creators.electrodes_header_extension_creator import ElectrodesHeaderExtensionCreator
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.injectors.electrodes_extension_injector import ElectrodesExtensionInjector
from src.datamigration.nwb_builder.managers.probe_manager import ProbeManager


class ElectrodeStructureBuilder:


def build_electrode_structure(header, metadata, nwb_content, probes):
    """
        For each electrode group in metadata.yml, check if device exist.
        If not create one.
        Create electrode_group
        Create electrodes from corresponding probe_type in probe.yml
    """

    device_counter = 0
    electrodes_builder = ElectrodesBuilder()
    electrodes_header_extension_creator = ElectrodesHeaderExtensionCreator().create_electrodes_header_extension(header)

    for electrode_group_metadata in metadata['electrode groups']:
        probe_metadata = ProbeManager().get_probe_file(probes, electrode_group_metadata['device_type'])

        device = DeviceCreator().create_device(probe_metadata, device_counter)
        device_counter += 1
        DeviceInjector(nwb_content).join_device(device)

        electrode_group = ElectrodeGroupBuilder().create_electrode_group(electrode_group_metadata, device)
        ElectrodeGroupInjector(nwb_content).join_electrode_group(electrode_group)

        electrodes_builder.build(probe_metadata, nwb_content, electrode_group)


    ElectrodesExtensionInjector().inject_extensions(
        nwb_content,
        electrodes_builder.get_electrodes_metadata_extension(),
        electrodes_header_extension_creator
    )



