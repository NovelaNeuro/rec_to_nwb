import os
import unittest
from pathlib import Path
from src.datamigration.xml_extractor import XMLExtractor

path = Path(__file__).parents[2]


#@unittest.skip("Need rec files")
class TestHeaderGenerations(unittest.TestCase):

    def setUp(self):
        self.xml_extractor = XMLExtractor(
            rec_path=path.name + '/test/test_data/beans/raw/20190718/20190718_beans_01_s1.rec',
            xml_path=path.name + 'header.xml',
            xsd_path=path.name + '/data/fl_lab_header.xsd'
        )

    def test_generation_xml(self):
        self.xml_extractor.extract_xml_from_rec_file()
        self.assertTrue(
            os.path.exists(
                'header.xml'
            )
        )

    def tearDown(self):
        if os.path.exists('header.xml'):
            os.remove('header.xml')
