
import os
from unittest import TestCase

from src.datamigration.nwb_components.device.probe_extractor import ProbesExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestProbeExtractor(TestCase):

    def setUp(self):
        self.probes_extractor = ProbesExtractor()
        self.probes = self.probes_extractor.extract_probes_metadata([path + '/res/probe1.yml',
                                             path + '/res/probe2.yml',
                                             path + '/res/probe3.yml'])

    def test_probes(self):
        self.assertEqual(3, len(self.probes))
        self.assertEqual('tetrode_12.5', self.probes[0]['probe_type'])