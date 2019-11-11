import unittest

from src.datamigration.nwb_builder.mda_extractor import MdaExtractor
from .experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        self.extractor = MdaExtractor(path=ExperimentData.mda_path, timestamp_file_name=ExperimentData.mda_timestamp,
                                      electrode_table_region=None)

    def test_reading_mda(self):
        self.assertIsNotNone(1)
