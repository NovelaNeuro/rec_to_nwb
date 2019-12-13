import os
import unittest

from rec_to_binaries import extract_trodes_rec_file

from .experiment_data import ExperimentData
from src.datamigration.nwb_file_builder import NWBFileBuilder


class TestRawToNWBGeneration(unittest.TestCase):

    def setUp(self):
        pass

    #@unittest.skip("Super heavy REC to Preprocessing Generation")
    def test_generation_preprocessing(self):
        extract_trodes_rec_file(ExperimentData.root_path, ExperimentData.animal_name, parallel_instances=4)
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path))
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path + "20190718"))

    def test_generation_nwb(self):
        self.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name='beans',
            date='20190718',
            dataset='01_s1',
            config_path='datamigration/res/metadata.yml',
        )
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)
        self.assertIsNotNone(self.nwbBuilder)
