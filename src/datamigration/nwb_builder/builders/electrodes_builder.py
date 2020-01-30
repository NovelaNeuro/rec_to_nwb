from src.datamigration.nwb_builder.creators.electrode_creator import ElectrodesCreator
from src.datamigration.nwb_builder.creators.electrode_metadata_extension_creator import ElectrodesMetadataExtensionCreator


class ElectrodesBuilder:
    def __init__(self):
        self.electrodes_creator = ElectrodesCreator()
        self.electrodes_metadata_extension_creator = ElectrodesMetadataExtensionCreator()
        self.electrodes_counter = 0

    def build(self, probe_metadata, nwb_content, electrode_group):
        for shank in probe_metadata['shanks']:
            for electrode in shank['electrodes']:
                self.electrodes_creator.create_electrode(nwb_content, electrode_group, self.electrodes_counter)
                self.electrodes_metadata_extension_creator.create_extensions(electrode)
                self.electrodes_counter += 1

    def get_electrodes_metadata_extension(self):
        return self.electrodes_metadata_extension_creator

