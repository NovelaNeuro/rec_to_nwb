import unittest
from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from .experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.extractor = MdaExtractor(path=ExperimentData.mda_path, timestamp_file_name=ExperimentData.mda_timestamp)

    def test_reading_mda(self):
        print(self.extractor.get_mda())
        self.assertTrue(False)
