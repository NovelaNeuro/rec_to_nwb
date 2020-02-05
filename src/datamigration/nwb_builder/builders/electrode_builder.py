from src.datamigration.nwb_builder.creators.electrode_creator import ElectrodesCreator
from src.datamigration.nwb_builder.creators.electrode_metadata_extension_creator import ElectrodesMetadataExtensionCreator
from src.datamigration.nwb_builder.creators.electrodes_header_extension_creator import ElectrodesHeaderExtensionCreator


class ElectrodesBuilder:
    def __init__(self):
        self.electrodes_creator = ElectrodesCreator()
        self.electrodes_metadata_extension_creator = ElectrodesMetadataExtensionCreator()
        self.electrodes_header_extension_creator = ElectrodesHeaderExtensionCreator()

    def build(self, electrode_groups, probes, probe_metadata, nwb_content, electrode_group):
        electrode_counter = 0
        for electrode_group in electrode_groups.values():
            for shank in probe_metadata['shanks']:
                for electrode in shank['electrodes']:


                    self.electrodes_creator.create_electrode_from_probe(nwb_content, electrode_group, self.electrodes_counter)

                self.electrodes_creator.create_electrode(nwb_content, electrode_group, self.electrodes_counter)
                self.electrodes_metadata_extension_creator.create_extensions(electrode)
                self.electrodes_counter += 1

        electrodes_header_extension = self.electrodes_header_extension_creator.create_electrodes_header_extension(
            self.header)
        electrodes_metadata_extension = self.electrodes_builder.get_electrodes_metadata_extension()  # todo build in separate place
        self.electrode_extension_injector.inject_extensions(  # todo put together injecting into nwb, but not here
            nwb_content,
            electrodes_metadata_extension,
            electrodes_header_extension
        )

    def get_electrodes_metadata_extension(self):
        return self.electrodes_metadata_extension_creator

