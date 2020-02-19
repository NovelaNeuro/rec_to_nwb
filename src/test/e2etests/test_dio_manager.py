import contextlib
import os
import unittest
from pathlib import Path
from unittest import mock
from unittest.mock import Mock

import pytest
from pandas import np

from src.datamigration.nwb.components.dio.dio_extractor import DioExtractor
from src.datamigration.nwb.components.dio.dio_files import DioFiles
from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb.components.dio.dio_manager import DioManager
from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = os.path.dirname(os.path.abspath(__file__))


# @unittest.skip('heave continuous time extraction')
class TestDioManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        continuous_time_dicts = [
            {1367266: 19191919, 9599570: 74747474, 9603169: 89898989, 9610303: 54545454, 9619154: 32323232,
             9612481: 67676767, 9619802: 50505050, 9627552: 41414141, 9643239: 23232323, 9644490: 21212121,
             9645544: 40404040, 9645721: 66666666, 9646074: 48484848, 9644629: 31313131, 9641056: 55555555}
        ]

        dio_metadata = [
            {'name': 'Din1', 'description': 'Poke1'},
            {'name': 'Din2', 'description': 'Poke2'}]

        dio_files = {
            'Din1': path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din1.dat',
            'Din2': path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din2.dat',
        }

        cls.dio_manager = DioManager(
            dio_files=dio_files,
            dio_metadata=dio_metadata,
            continuous_time_dicts=continuous_time_dicts)

        cls.mock_din_1_array = Mock()
        cls.mock_din_1_array.__class__ = np.array
        cls.mock_din_1_list = Mock()
        cls.mock_din_1_list.__class__ = list

        cls.mock_din_2_array = Mock()
        cls.mock_din_2_array.__class__ = np.array
        cls.mock_din_2_list = Mock()
        cls.mock_din_2_list.__class__ = list

        cls.dio_manager.dio_extractor = Mock()
        cls.dio_manager.dio_extractor.__class__ = DioExtractor
        # cls.dio_manager.dio_extractor.extract_dio_for_single_dataset().return_value = {
        #     'Din1': [mock_din_1_array, mock_din_1_list],
        #     'Din2': [mock_din_2_array, mock_din_2_list],
        # }

    @mock.patch('dio_manager.extract_dio_for_single_dataset')
    def test_get_dio_returnCorrectType_true(self, mock_method):
        mock_method.return_value = {
            'Din1': [self.mock_din_1_array, self.mock_din_1_list],
            'Din2': [self.mock_din_2_array, self.mock_din_2_list],
        }
        self.dio_manager.dio_extractor.extract_dio_for_single_dataset()
        self.assertIsInstance(list, self.dio_manager.get_dio())
        self.assertIsInstance(dict, self.dio_manager.get_dio()[0])

    # def test_dio_extractor(self):
    #     dio_data = self.dio_manager.get_dio()
    #     self.assertIsNotNone(dio_data)
    #     self.assertEqual(2, len(dio_data))
