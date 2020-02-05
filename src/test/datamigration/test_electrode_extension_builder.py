import os
from unittest import TestCase

from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.builders.electrode_extension_builder import ElectrodeExtensionBuilder
from src.datamigration.nwb_builder.creators.electrode_metadata_extension_creator import \
    ElectrodesMetadataExtensionCreator
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestElectrodeExtensionsBuilder(TestCase):

    def setUp(self):
        self.metadata = NWBMetadata(str(path) + '/res/nwb_elements_builder_test/metadata.yml',
                                    [str(path) + '/res/nwb_elements_builder_test/probe1.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe2.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe3.yml'])
        self.header = Header(str(path) + '/res/nwb_elements_builder_test/header.xml')

        self.electrode_extension_builder = ElectrodeExtensionBuilder(
            probes_metadata=self.metadata.probes,
            electrode_groups_metadata=self.metadata.metadata['electrode groups'],
            header=self.header
        )

    def test_build_successful_creation(self):

        electrodes_metadata_extension, electrodes_header_extension = self.electrode_extension_builder.build()

        self.assertIsInstance(electrodes_metadata_extension, ElectrodesMetadataExtensionCreator)
        self.assertIsInstance(electrodes_header_extension, list)
