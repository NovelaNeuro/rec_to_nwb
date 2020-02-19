import contextlib
import os
import unittest
from pathlib import Path
from unittest.mock import Mock

import pytest
from pandas import np
from testfixtures import tempdir

from src.datamigration.nwb.components.dio.dio_extractor import DioExtractor
from src.datamigration.nwb.components.dio.dio_files import DioFiles
from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb.components.dio.dio_manager import DioManager
from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip('heave continuous time extraction')
class TestDioManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        continuous_time_dicts = [{
            1367266: 19191919, 9599570: 74747474, 9603169: 89898989, 9610303: 54545454, 9619154: 32323232,
            9612481: 67676767, 9619802: 50505050, 9627552: 41414141, 9643239: 23232323, 9644490: 21212121,
            9645544: 40404040, 9645721: 66666666, 9646074: 48484848, 9644629: 31313131, 9641056: 55555555}]

        dio_metadata = [
            {'name': 'Din1', 'description': 'Poke1'},
            {'name': 'Din2', 'description': 'Poke2'}]

        dio_directory = str(path) + '/datamigration/res/dio_test'

        dio_files = [
            {
            }
        ]

        cls.dio_manager = DioManager(
            dio_files=mock_dio_files,
            dio_metadata=dio_metadata,
            continuous_time_dicts=continuous_time_dicts)

        mock_din_1_array = Mock()
        mock_din_1_array.__class__ = np.array
        mock_din_1_list = Mock()
        mock_din_1_list.__class__ = list

        mock_din_2_array = Mock()
        mock_din_2_array.__class__ = np.array
        mock_din_2_list = Mock()
        mock_din_2_list.__class__ = list

        cls.dio_manager.dio_extractor = Mock()
        cls.dio_manager.dio_extractor.__class__ = DioExtractor
        cls.dio_manager.dio_extractor.extract_dio_for_single_dataset().return_value = {
            'Din1': [mock_din_1_array, mock_din_1_list],
            'Din2': [mock_din_2_array, mock_din_2_list],
        }

    def test_get_dio_returnCorrectType_true(self):
        self.assertIsInstance(list, self.dio_manager.get_dio())
        self.assertIsInstance(dict, self.dio_manager.get_dio()[0])
    # def test_dio_extractor(self):
    #     dio_data = self.dio_manager.get_dio()
    #     self.assertIsNotNone(dio_data)
    #     self.assertEqual(2, len(dio_data))
