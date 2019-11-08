import unittest
from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataExtractor(configuration_path='../metadata.yml')

    def test_reading_metadata(self):
        self.assertEqual('hulk', self.metadata.experimenter_name)