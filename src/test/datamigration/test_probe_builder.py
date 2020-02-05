import os
from unittest import TestCase

from src.datamigration.nwb_builder.builders.probe_builder import ProbesDictBuilder
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata

path = os.path.dirname(os.path.abspath(__file__))


class TestProbeBuilder(TestCase):

    def setUp(self):
        self.metadata = NWBMetadata(str(path) + '/res/probe_builder_test/metadata.yml',
                                    [str(path) + '/res/probe_builder_test/probe1.yml',
                                     str(path) + '/res/probe_builder_test/probe2.yml',
                                     str(path) + '/res/probe_builder_test/probe3.yml'])

        self.probes_builder = ProbesDictBuilder(probes_metadata=self.metadata.probes)

    def test_build(self):
        self.probes_dict = self.probes_builder.build(
            electrode_groups_metadata=self.metadata.metadata['electrode groups'],
        )
