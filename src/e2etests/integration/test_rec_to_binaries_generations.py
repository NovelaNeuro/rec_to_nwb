import os
import unittest

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.xml_extractor import XMLExtractor
from src.e2etests.integration.experiment_data import ExperimentData


class TestRecToBinGeneration(unittest.TestCase):

    def setUp(self):
        print('Test requires test_data folder with raw folder at e2etests location')

    def test_generation_preprocessing(self):
        extract_trodes_rec_file(ExperimentData.root_path, ExperimentData.animal_name, parallel_instances=4)
        assert os.path.isdir(ExperimentData.preprocessing_root_path) == 1
        assert os.path.isdir(ExperimentData.preprocessing_root_path + "20190718") == 1

    def test_generation_xml(self):
        xml_extractor = XMLExtractor(
            rec_path=ExperimentData.rec_path,
            xml_path=ExperimentData.preprocessing_root_path + ExperimentData.date + ExperimentData.xml_file,
            xsd_path=ExperimentData.xsd_path
        )
        xml_extractor.extract_xml_from_rec_file()
        assert os.path.exists(
            ExperimentData.preprocessing_root_path + ExperimentData.date + ExperimentData.xml_file) == 1
