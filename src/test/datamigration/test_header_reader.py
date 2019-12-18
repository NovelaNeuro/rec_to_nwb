import os
import unittest

from src.datamigration.nwb_builder.header_checker.header_reader import HeaderReader

path = os.path.dirname(os.path.abspath(__file__))


class TestHeaderReader(unittest.TestCase):

    def setUp(self):
        with open(path + '/res/test_xmls/test1.xml', 'w') as xml_1:
            xml_1.write('string string string')
        xml_2 = open(path + '/res/test_xmls/test2.xml', 'w')
        xml_2.write('random test strings')
        xml_3 = open(path + '/res/test_xmls/test3.xml', 'w')
        xml_3.write('some content')
        self.header_reader = HeaderReader([path + '/res/test_xmls/test1.xml',
                                           path + '/res/test_xmls/test2.xml',
                                           path + '/res/test_xmls/test3.xml']
                                          )

    def test_reading_headers(self):
        headers_content = self.header_reader.read_headers()
        self.assertNotEqual([], headers_content)
        self.assertIsNotNone(headers_content[2])
        self.assertNotEqual('', headers_content[0])
        self.assertEqual(3, len(headers_content))
        self.assertEqual('some content', headers_content[2])
        self.assertEqual('random test strings', headers_content[1])
        self.assertEqual('string string string', headers_content[0])

