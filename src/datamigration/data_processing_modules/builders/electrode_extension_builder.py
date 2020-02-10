from src.datamigration.data_processing_modules.creators.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator
from src.datamigration.data_processing_modules.creators.electrodes_header_extension_creator import \
    ElectrodesHeaderExtensionCreator
from src.datamigration.tools.filter_probe_by_type import filter_probe_by_type


class ElectrodeExtensionBuilder:
    def __init__(self, probes_metadata, electrode_groups_metadata, header):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata
        self.header = header

        self.electrodes_metadata_extension_creator = ElectrodesMetadataExtensionCreator()
        self.electrodes_header_extension_creator = ElectrodesHeaderExtensionCreator()

    def build(self):
        self._create_extension_from_metadata(self.electrode_groups_metadata, self.probes_metadata)

        electrodes_header_extension = self.electrodes_header_extension_creator.create_electrodes_header_extension(self.header)
        electrodes_metadata_extension = self.electrodes_metadata_extension_creator
        return electrodes_metadata_extension, electrodes_header_extension

    def _create_extension_from_metadata(self, electrode_groups_metadata, probes_metadata):
        for electrode_group_metadata in electrode_groups_metadata:
            probe_metadata = filter_probe_by_type(probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for electrode in shank['electrodes']:
                    self.electrodes_metadata_extension_creator.create_extensions(electrode)