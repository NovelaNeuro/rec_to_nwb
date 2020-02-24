import os
import unittest

import numpy as np

from src.datamigration.nwb_builder.extractors.mda_extractor import MdaExtractor
from src.datamigration.utils.file_scanner import Dataset

path = os.path.dirname(os.path.abspath(__file__))


@unittest.skip("test requires continuoustime.dat file and can't be used on travis")
class TestMDAExtraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = os.path.dirname(os.path.abspath(__file__))

    def test_reading_mda(self):
        self.dataset = self.create_test_dataset()
        mda_extractor = MdaExtractor([self.dataset])
        series = mda_extractor.get_mda_data()
        self.assertEqual(100, np.size(series.mda_timestamps, 0))
        self.assertEqual(12, np.size(series.mda_data, 1))
        self.assertEqual(5, np.size(series.mda_data, 0))

    def create_test_dataset(self):
        dataset = Dataset('test_dataset')
        dataset.add_data_to_dataset(self.path + '/../datamigration/res/mda_test/', 'mda')
        dataset.add_data_to_dataset(path + '/../test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/',
                                    'time')
        return dataset
