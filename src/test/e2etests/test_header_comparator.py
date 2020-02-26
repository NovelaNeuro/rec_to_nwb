import os
import unittest

from src.datamigration.header.header_checker.header_comparator import HeaderComparator

path = os.path.dirname(os.path.abspath(__file__))


class TestHeaderComparator(unittest.TestCase):

    @unittest.skip('test need to create files localy not working on travis')
    class TestHeaderReader(unittest.TestCase):

        def setUp(self):
            with open(path + '/../datamigration/res/test_xmls/test1.xml', 'w') as xml_1:
                xml_1.write('<string_string_string/>')
            with open(path + '/../datamigration//res/test_xmls/test2.xml', 'w') as xml_2:
                xml_2.write('<random_test_strings/>')
            with open(path + '/../datamigration//res/test_xmls/test3.xml', 'w') as xml_3:
                xml_3.write('<some_content/>')
            self.header_comparator = HeaderComparator([path + '/../datamigration/res/test_xmls/test1.xml',
                                                       path + '/../datamigration/res/test_xmls/test2.xml',
                                                       path + '/../datamigration/res/test_xmls/test3.xml']
                                                       )

        def test_comparing_headers(self):
            headers_difference = self.header_comparator.compare()
            self.assertNotEqual([], headers_difference)
