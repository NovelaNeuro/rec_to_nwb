import os
import unittest
from pathlib import Path

from lf.datamigration.header.header_checker.header_extractor import HeaderFilesExtractor

path = Path(__file__).parent.parent
path.resolve()


@unittest.skip('test need rec files localy not working on travis')
class TestHeaderReader(unittest.TestCase):

    def setUp(self):
        self.rec_files = [
                    str(path) + '/test_data/beans/raw/20190718/20190718_beans_01_s1.rec',
                    str(path) + '/test_data/beans/raw/20190718/20190718_beans_02_r1.rec',
                    str(path) + '/test_data/beans/raw/20190718/20190718_beans_03_s2.rec',
                    str(path) + '/test_data/beans/raw/20190718/20190718_beans_04_r2.rec',
                    ]
        self.header_extractor = HeaderFilesExtractor()

    def test_extraction_from_rec_files(self):
        self.xml_files = self.header_extractor.extract_headers_from_rec_files(self.rec_files)
        self.assertEqual(4, len(self.xml_files))
        self.assertEqual([
                            str(path) + '/test_data/beans/raw/20190718/20190718_beans_01_s1.rec_header.xml',
                            str(path) + '/test_data/beans/raw/20190718/20190718_beans_02_r1.rec_header.xml',
                            str(path) + '/test_data/beans/raw/20190718/20190718_beans_03_s2.rec_header.xml',
                            str(path) + '/test_data/beans/raw/20190718/20190718_beans_04_r2.rec_header.xml'
                         ],
                         self.xml_files)

    def tearDown(self):
        for xml_file in self.xml_files:
            os.remove(xml_file)