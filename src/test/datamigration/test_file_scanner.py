import os
import unittest

import src.datamigration.file_scanner as fs
from src.test.e2etests.experiment_data import ExperimentData


class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.data_folder = fs.DataScanner(ExperimentData.root_path)

    @unittest.skip("DOES NOT WORK!!!")
    def test_scanner(self):
        self.assertEqual(ExperimentData.pos_path,
                         self.data_folder.data['beans']['20190718']['01_s1'].get_data_path_from_dataset('pos'))
        self.assertEqual(len(self.data_folder.data['beans']['20190718']['01_s1'].get_all_data_from_dataset('mda')),
                         len(os.listdir(ExperimentData.mda_path)))
        self.assertEqual(ExperimentData.mda_path,
                         self.data_folder.data['beans']['20190718']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual(len(self.data_folder.data['beans']['20190718']['01_s1'].get_all_data_from_dataset('metadata')),
                         1)

        # self.assertEqual(['beans'], self.data_folder.get_all_animals())
        # self.assertEqual(['20190718'], self.data_folder.get_all_experiment_dates('beans'))
        # self.assertEqual(['01_s1'], self.data_folder.get_all_datasets('beans', '20190718'))
