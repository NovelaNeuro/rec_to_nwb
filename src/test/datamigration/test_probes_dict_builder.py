import os
from unittest import TestCase

from src.datamigration.extension.probe import Probe
from src.datamigration.nwb_builder.builders.probes_dict_builder import ProbesDictBuilder
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestProbesDictBuilder(TestCase):

    def setUp(self):
        self.metadata = NWBMetadata(str(path) + '/res/nwb_elements_builder_test/metadata.yml',
                                    [str(path) + '/res/nwb_elements_builder_test/probe1.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe2.yml',
                                     str(path) + '/res/nwb_elements_builder_test/probe3.yml'])

        self.probes_builder = ProbesDictBuilder(
            probes_metadata=self.metadata.probes,
            electrode_groups_metadata=self.metadata.metadata['electrode groups']
        )

    def test_build_successful_creation(self):
        probes_dict = self.probes_builder.build()

        self.assertEqual(2, len(probes_dict))
        self.assertIsInstance(probes_dict[0], Probe)
        self.assertIsInstance(probes_dict[1], Probe)