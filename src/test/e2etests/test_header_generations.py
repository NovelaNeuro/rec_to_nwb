import os
import unittest
from pathlib import Path

from src.datamigration.xml_extractor import XMLExtractor

path = Path(__file__).parent.parent
path.resolve()



@unittest.skip("Need rec files")
class TestHeaderGenerations(unittest.TestCase):

    def setUp(self):
        self.xml_extractor = XMLExtractor(
            rec_path=str(path) + '/test_data/beans/raw/20190718/20190718_beans_01_s1.rec',
            xml_path='header.xml',
            xsd_path=str(path.parent) + '/data/fl_lab_header.xsd'
        )

    @unittest.skip("Need rec files")
    def test_generation_xml(self):
        self.xml_extractor.extract_xml_from_rec_file()
        self.assertTrue(
            os.path.exists('header.xml'))

    def tearDown(self):
        if os.path.exists('header.xml'):
            os.remove('header.xml')
