import os
import unittest
from unittest import TestCase
import pandas as pd

from fl.datamigration.nwb.components.dio.dio_extractor import DioExtractor

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip('Need preprocessed .dat files')
class TestDioExtractor(TestCase):

    @classmethod
    def setUpClass(cls):
        continuoues_time_dict = {
            '1367266': 19191919, '9599570': 74747474, '9603169': 89898989, '9610303': 54545454, '9619154': 32323232,
            '9612481': 67676767, '9619802': 50505050, '9627552': 41414141, '9643239': 23232323, '9644490': 21212121,
            '9645544': 40404040, '9645721': 66666666, '9646074': 48484848, '9644629': 31313131, '9641056': 55555555
        }

        filtered_files = {
            'Din1': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din1.dat',
            'Din2': path + '/../../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO//20190718_beans_01_s1.dio_Din2.dat',
        }

        cls.single_dataset_data = DioExtractor.extract_dio_for_single_dataset(
            filtered_files=filtered_files,
            continuoues_time_dict=continuoues_time_dict
        )

    def test_extracted_dio_for_single_dataset_correctType_true(self):
        self.assertIsInstance(self.single_dataset_data, dict)
        self.assertIsInstance(self.single_dataset_data['Din1'], list)
        self.assertIsInstance(self.single_dataset_data['Din1'][0], pd.ndarray)
        self.assertIsInstance(self.single_dataset_data['Din1'][1], list)

        self.assertIsInstance(self.single_dataset_data['Din2'], list)
        self.assertIsInstance(self.single_dataset_data['Din2'][0], pd.ndarray)
        self.assertIsInstance(self.single_dataset_data['Din2'][1], list)

    def test_extracted_dio_for_single_dataset_correctValues_true(self):
        self.assertEqual(
            self.single_dataset_data,
            {
                'Din1': [
                    array([
                        0.01919192, 0.07474747, 0.08989899, 0.05454545, 0.06767677,
                        0.03232323, 0.05050505, 0.04141414, 0.05555555, 0.02323232,
                        0.02121212, 0.03131313, 0.04040404, 0.06666667, 0.04848485
                    ]),
                    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]],
                'Din2': [
                    array([0.01919192]),
                    [0]]}
        )
        self.assertEqual(
            self.single_dataset_data['Din1'][0],
            array([
                0.01919192, 0.07474747, 0.08989899, 0.05454545, 0.06767677,
                0.03232323, 0.05050505, 0.04141414, 0.05555555, 0.02323232,
                0.02121212, 0.03131313, 0.04040404, 0.06666667, 0.04848485
            ])
        )
        self.assertEqual(
            self.single_dataset_data['Din1'][1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
        )
        self.assertEqual(
            self.single_dataset_data['Din2'][0],
            array([0.01919192])
        )
        self.assertEqual(
            self.single_dataset_data['Din2'][1],
            [0]
        )

    def test_extracted_dio_for_single_dataset_returnCorrectShape_true(self):
        self.assertEqual(len(self.single_dataset_data), 2)

        self.assertEqual(len(self.single_dataset_data['Din1']), 2)
        self.assertEqual(self.single_dataset_data['Din1'][0].shape, (15,))
        self.assertEqual(len(self.single_dataset_data['Din1'][1]), 15)

        self.assertEqual(len(self.single_dataset_data['Din2']), 2)
        self.assertEqual(self.single_dataset_data['Din2'][0].shape, (1,))
        self.assertEqual(len(self.single_dataset_data['Din2'][1]), 1)
