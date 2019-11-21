import os
import unittest

import src.datamigration.file_scanner as fs
from .experiment_data import ExperimentData


class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.data_folder = fs.DataScanner(ExperimentData.root_path)

    def test_scanner(self):
        self.assertEqual(ExperimentData.pos_path,
                         self.data_folder.data['jaq']['20190911']['01_s1'].get_data_path_from_dataset('pos'))
        self.assertEqual(len(self.data_folder.data['jaq']['20190911']['01_s1'].get_all_data_from_dataset('mda')),
                         len(os.listdir(ExperimentData.mda_path)))
        self.assertEqual(ExperimentData.mda_path,
                         self.data_folder.data['jaq']['20190911']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual(len(self.data_folder.data['jaq']['20190911']['01_s1'].get_all_data_from_dataset('metadata')),
                         1)

        # self.assertEqual(['jaq'], self.data_folder.get_all_animals())
        # self.assertEqual(['20190911'], self.data_folder.get_all_experiment_dates('jaq'))
        # self.assertEqual(['01_s1'], self.data_folder.get_all_datasets('jaq', '20190911'))
