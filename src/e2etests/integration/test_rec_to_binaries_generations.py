import os
import unittest

from rec_to_binaries import extract_trodes_rec_file

from src.e2etests.integration.experiment_data import ExperimentData


class TestRecToBinGeneration(unittest.TestCase):

    def setUp(self):
        print('Test requires test_data folder with raw folder at e2etests location')

    def test_generation_preprocessing(self):
        extract_trodes_rec_file(ExperimentData.root_path, ExperimentData.animal_name, parallel_instances=4)
        assert os.path.isdir(ExperimentData.preprocessing_root_path) == 1
        assert os.path.isdir(ExperimentData.preprocessing_root_path + "20190718") == 1
