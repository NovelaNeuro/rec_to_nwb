import os
import unittest

from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator

path = os.path.dirname(os.path.abspath(__file__))


class TestHeaderComparator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.list_with_diferent_strings = ['first string representing content',
                                          'another string representing content',
                                          'another string representing content']
        cls.list_with_same_strings = ['string representing content',
                                      'string representing content',
                                      'string representing content']

        cls.list_with_one_string = ['string only one but powerful']

    def test_comparing_diferent_headers(self):
        header_comparator = HeaderComparator(self.list_with_diferent_strings)
        self.assertFalse(header_comparator.compare())

    def test_comparing_same_headers(self):
        header_comparator = HeaderComparator(self.list_with_same_strings)
        self.assertTrue(header_comparator.compare())

    def test_comparing_one_header(self):
        header_comparator = HeaderComparator(self.list_with_one_string)
        self.assertTrue(header_comparator.compare())

