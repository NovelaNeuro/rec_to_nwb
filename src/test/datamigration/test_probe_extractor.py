
import os
from unittest import TestCase

from src.datamigration.nwb_builder.extractors.probe_extractor import ProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestProbeExtractor(TestCase):

    def setUp(self):
        self.probes = ProbesExtractor()
        self.probes.extract_probes_metadata([path + '/res/probe1.yml',
                                             path + '/res/probe2.yml',
                                             path + '/res/probe3.yml'])

    def test_probes(self):
        self.assertEqual(3, len(self.probes.probes_content))
        self.assertEqual('tetrode_12.5', self.probes.probes_content[0]['probe_type'])