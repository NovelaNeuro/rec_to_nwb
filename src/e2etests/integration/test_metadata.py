import unittest

from src.datamigration.nwb.metadata_extractor import MetadataExtractor


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataExtractor(configuration_path='../metadata.yml')

    def test_reading_metadata(self):
        self.assertEqual('hulk', self.metadata.experimenter_name)
        # todo add the rest of the properties, I know it is painful

    # todo add test with creating nwb_builder with the values taken from metadata.yml in separated file.
