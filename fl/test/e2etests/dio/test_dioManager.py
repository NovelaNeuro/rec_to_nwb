import os
import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from pandas import array

from fl.datamigration.nwb.components.dio.dio_extractor import DioExtractor
from fl.datamigration.nwb.components.dio.dio_manager import DioManager

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip('Need preprocessed .dat files')
class TestDioManager(unittest.TestCase):

    @staticmethod
    def fake_extract_dio_for_single_dataset(*args, **kwargs):
        return {
            'Din1': [
                array(
                    [0.01919192, 0.07474747, 0.08989899, 0.05454545, 0.06767677,
                     0.03232323, 0.05050505, 0.04141414, 0.05555555, 0.02323232,
                     0.02121212, 0.03131313, 0.04040404, 0.06666667, 0.04848485]
                ),
                [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
            ],
            'Din2': [
                array(
                    [0.01919192]
                ),
                [0]
            ]
        }

    @classmethod
    @patch.object(DioExtractor, 'extract_dio_for_single_dataset', new=fake_extract_dio_for_single_dataset)
    def setUpClass(cls):
        dio_metadata = [
            {'name': 'Din1', 'description': 'Poke1'},
            {'name': 'Din2', 'description': 'Poke2'}
        ]

        dio_files = [
            {
                'Din1': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din1.dat',
                'Din2': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din2.dat',
            },
            {
                'Din1': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din1.dat',
                'Din2': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din2.dat',
            },
        ]

        cls.dio_manager = DioManager(
            dio_files=dio_files,
            dio_metadata=dio_metadata,
            continuous_time_files='mocked'
        )

        cls.din_1_array = pd.array(
            [1367266, 9599570, 9603169, 9610303, 9612481,
             9619154, 9619802, 9627552, 9641056, 9643239,
             9644490, 9644629, 9645544, 9645721, 9646074]
        )
        cls.din_1_list = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

        cls.din_2_array = pd.array([1367266])
        cls.din_2_list = [0]

        cls.dio_manager.dio_extractor = Mock(spec=DioExtractor)
        cls.dio_manager.dio_extractor.extract_dio_for_single_dataset.return_value = {
            'Din1': [cls.din_1_array, cls.din_1_list],
            'Din2': [cls.din_2_array, cls.din_2_list],
        }
        cls.dio = cls.dio_manager.get_dio()

    def test_get_dio_returnCorrectType_true(self):
        self.assertIsInstance(self.dio, dict)
        self.assertIsInstance(self.dio['Din1'][0], np.ndarray)
        self.assertIsInstance(self.dio['Din1'][1], list)
        self.assertIsInstance(self.dio['Din2'][0], np.ndarray)
        self.assertIsInstance(self.dio['Din2'][1], list)

    def test_get_dio_returnCorrectValue_true(self):
        self.assertEqual(
            self.dio,
            {
                'Din1': [
                    array([
                        1367266, 9599570, 9603169, 9610303, 9612481, 9619154, 9619802,
                        9627552, 9641056, 9643239, 9644490, 9644629, 9645544, 9645721,
                        9646074, 1367266, 9599570, 9603169, 9610303, 9612481, 9619154,
                        9619802, 9627552, 9641056, 9643239, 9644490, 9644629, 9645544,
                        9645721, 9646074
                    ]),
                    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]],
                'Din2': [
                    array([1367266, 1367266]),
                    [0, 0]
                ]
            }
        )
        self.assertEqual(
            self.dio['Din1'][0],
            array([
                1367266, 9599570, 9603169, 9610303, 9612481, 9619154, 9619802,
                9627552, 9641056, 9643239, 9644490, 9644629, 9645544, 9645721,
                9646074, 1367266, 9599570, 9603169, 9610303, 9612481, 9619154,
                9619802, 9627552, 9641056, 9643239, 9644490, 9644629, 9645544,
                9645721, 9646074
            ])
        )
        self.assertEqual(
            self.dio['Din1'][1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        )
        self.assertEqual(
            self.dio['Din2'][0],
            array([1367266, 1367266])
        )
        self.assertEqual(
            self.dio['Din2'][1],
            [0, 0]
        )

    def test_get_dio_returnCorrectShape_true(self):
        self.assertEqual(len(self.dio), 2)

        self.assertEqual(len(self.dio['Din1']), 2)
        self.assertEqual(self.dio['Din1'][0].shape, (30,))
        self.assertEqual(len(self.dio['Din1'][1]), 30)

        self.assertEqual(len(self.dio['Din2']), 2)
        self.assertEqual(self.dio['Din2'][0].shape, (2,))
        self.assertEqual(len(self.dio['Din2'][0]), 2)
        self.assertEqual(len(self.dio['Din2'][1]), 2)
