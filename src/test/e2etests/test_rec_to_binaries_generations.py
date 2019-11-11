import os
import unittest

from rec_to_binaries import extract_trodes_rec_file

from .experiment_data import ExperimentData


class TestRecToBinGeneration(unittest.TestCase):

    def setUp(self):
        pass

    def test_generation_preprocessing(self):
        extract_trodes_rec_file(ExperimentData.root_path, ExperimentData.animal_name, parallel_instances=4)
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path))
        self.assertTrue(os.path.isdir(ExperimentData.preprocessing_root_path + "20190718"))
