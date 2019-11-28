import unittest

from src.datamigration.nwb_file_builder import NWBFileBuilder
from .experiment_data import ExperimentData


class TestNwbFullGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            config_path='datamigration/res/metadata.yml',
            header_path='datamigration/res/fl_lab_sample_header.xml')

    def test_generate_nwb(self):
        self.assertIsNotNone(cls.nwbBuilder)

    @classmethod
    def tearDownClass(cls):
        del cls.nwbBuilder
