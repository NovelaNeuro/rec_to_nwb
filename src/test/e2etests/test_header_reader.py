import os
import unittest

from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_reader import HeaderReader

path = os.path.dirname(os.path.abspath(__file__))


#@unittest.skip('test need to create files localy not working on travis')
class TestHeaderReader(unittest.TestCase):

    def setUp(self):
        with open(path + '/../datamigration/res/test_xmls/test1.xml', 'w') as xml_1:
            xml_1.write('<string_string_string/>')
        with open(path + '/../datamigration//res/test_xmls/test2.xml', 'w') as xml_2:
            xml_2.write('<random_test_strings/>')
        with open(path + '/../datamigration//res/test_xmls/test3.xml', 'w') as xml_3:
            xml_3.write('<some_content/>')
        self.header_reader = HeaderReader([path + '/../datamigration/res/test_xmls/test1.xml',
                                           path + '/../datamigration/res/test_xmls/test2.xml',
                                           path + '/../datamigration/res/test_xmls/test3.xml']
                                          )

    def test_reading_headers(self):
        headers_content = self.header_reader.read_headers()
        self.assertNotEqual([], headers_content)
        self.assertIsNotNone(headers_content[2])
        self.assertNotEqual('', headers_content[0])
        self.assertEqual(3, len(headers_content))
        self.assertEqual('<some_content/>', headers_content[2])
        self.assertEqual('<random_test_strings/>', headers_content[1])
        self.assertEqual('<string_string_string/>', headers_content[0])

