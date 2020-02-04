from src.datamigration.nwb_builder.builders.electrodes_builder import ElectrodesBuilder
from src.datamigration.nwb_builder.creators.electrode_group_creator import ElectrodeGroupBuilder
from src.datamigration.nwb_builder.creators.electrodes_header_extension_creator import ElectrodesHeaderExtensionCreator
from src.datamigration.nwb_builder.creators.probe_creator import ProbeCreator
from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor
from src.datamigration.nwb_builder.injectors.device_injector import DeviceInjector
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.injectors.electrodes_extension_injector import ElectrodesExtensionInjector


class ElectrodeStructureBuilder:  # todo rething this class || make this singleton
    def __init__(self, header, metadata, probes_paths):
        self.header = header
        self.metadata = metadata
        self.probe_extractor = ProbesExtractor()
        self.probe_extractor.extract_probes_metadata(probes_paths)

        self.electrode_extension_injector = ElectrodesExtensionInjector()
        self.electrodes_builder = ElectrodesBuilder()
        self.electrodes_header_extension_creator = ElectrodesHeaderExtensionCreator()
        self.probe_creator = ProbeCreator()

    def build(self, nwb_content):
        """
            For each electrode group in metadata.yml, check if probe exist.
            If not create one.
            Create electrode_group
            Create electrodes from corresponding probe_type in probe.yml
        """

        probe_counter = 0
        electrodes_header_extension = self.electrodes_header_extension_creator.create_electrodes_header_extension(self.header)

        for electrode_group_metadata in self.metadata['electrode groups']:
            probe_metadata = self.probe_extractor.get_probe_file(electrode_group_metadata['device_type'])

            probe = self.probe_creator.create_probe(probe_metadata, probe_counter)
            probe_counter += 1
            DeviceInjector(nwb_content).join_device(probe)#todo do not inject here, just build the list of probes

            electrode_group = ElectrodeGroupBuilder().create_electrode_group(electrode_group_metadata, probe)#todo build electrode groups in separate place as well as injecting into nwb
            ElectrodeGroupInjector(nwb_content).join_electrode_group(electrode_group)

            self.electrodes_builder.build(probe_metadata, nwb_content, electrode_group)

        electrodes_metadata_extension = self.electrodes_builder.get_electrodes_metadata_extension()#todo build in separate place
        self.electrode_extension_injector.inject_extensions(#todo put together injecting into nwb, but not here
            nwb_content,
            electrodes_metadata_extension,
            electrodes_header_extension
        )
