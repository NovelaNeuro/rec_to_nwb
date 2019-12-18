import os
import unittest

from src.datamigration.nwb_builder.header_checker.header_reader import HeaderReader

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip('local test need to be launched with e2etests')
class TestHeaderReader(unittest.TestCase):

    def setUp(self):
        with open(path + '/res/test_xmls/test1.xml', 'a+') as xml_1:
            xml_1.write('string string string')
        with open(path + '/res/test_xmls/test2.xml', 'a+') as xml_2:
            xml_2.write('random test strings')
        with open(path + '/res/test_xmls/test3.xml', 'a+') as xml_3:
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

