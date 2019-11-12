import os
import unittest

from src.datamigration.xml_extractor import XMLExtractor
from src.test.e2etests.experiment_data import ExperimentData


class TestHeaderGenerations(unittest.TestCase):

    def setUp(self):
        self.xml_extractor = XMLExtractor(
            rec_path=ExperimentData.rec_path,
            xml_path=ExperimentData.preprocessing_root_path + ExperimentData.date + ExperimentData.xml_file,
            xsd_path=ExperimentData.xsd_path
        )

    def test_generation_xml(self):
        self.xml_extractor.extract_xml_from_rec_file()
        self.assertTrue(os.path.exists(
            ExperimentData.preprocessing_root_path + ExperimentData.date + ExperimentData.xml_file
        ))
