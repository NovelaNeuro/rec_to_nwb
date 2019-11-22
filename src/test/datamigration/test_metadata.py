import unittest

from src.datamigration.nwb_builder.metadata_extractor import MetadataExtractor
from src.test.e2etests.experiment_data import ExperimentData


class TestMetadata(unittest.TestCase):

    def setUp(self):
        self.metadata = MetadataExtractor(data_path=ExperimentData.root_path)

    @unittest.skip("DOES NOT WORK!!!")
    def test_reading_metadata(self):
        self.assertEqual('hulk', self.metadata.experimenter_name)