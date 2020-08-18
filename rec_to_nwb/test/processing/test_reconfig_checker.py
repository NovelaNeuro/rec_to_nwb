import os
import unittest

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.header.reconfig_header_checker import ReconfigHeaderChecker


path = os.path.dirname(os.path.abspath(__file__))


class TestReconfigChecker(unittest.TestCase):

    def test_validation_correct_header_path(self):
        xml_header_path = str(path) + '/res/reconfig_header.xml'

        validated_path = ReconfigHeaderChecker.validate(xml_header_path)

        self.assertEqual(validated_path, xml_header_path)

    @should_raise(MissingDataException)
    def test_validation_incorrect_header_path(self):
        xml_header_path = str(path) + '/res/reconfig_header111.xml'

        ReconfigHeaderChecker.validate(xml_header_path)

    def test_validation_empty_path(self):
        xml_header_path = ''

        validated_path = ReconfigHeaderChecker.validate(xml_header_path)

        self.assertEqual(validated_path, None)