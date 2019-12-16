import os
import unittest

from .experiment_data import ExperimentData
from src.datamigration.raw_to_nwb_builder import RawToNWBBuilder


@unittest.skip("Super heavy RAW to NWB Generation")
class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        self.builder = RawToNWBBuilder(animal_name='beans',
                                       date='20190718',
                                       dataset='01_s1',
                                       metadata_path=ExperimentData.metadata_path,
                                       )

    def test_from_raw_to_nwb_generation(self):
        self.builder.extract_data()
        self.builder.build_nwb()
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path))
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path + "20190718"))

    def tearDown(self):
        self.builder._cleanup()
