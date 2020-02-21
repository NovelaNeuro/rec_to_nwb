import os
from unittest import TestCase

from src.datamigration.nwb.components.device.probe_extractor import ProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))

# ToDo mock yaml files
class TestProbeExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.probes_extractor = ProbesExtractor()
        cls.probes_content = cls.probes_extractor.extract_probes_metadata(
            [
                path + '/res/probe1.yml',
                path + '/res/probe2.yml',
                path + '/res/probe3.yml'
            ]
        )

    def test_extractProbesMetadata_successful_true(self):
        self.assertIsNotNone(self.probes_content)
