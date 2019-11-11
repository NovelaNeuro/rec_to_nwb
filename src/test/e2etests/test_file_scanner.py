import unittest

import src.datamigration.file_scanner as fs
from src.test.e2etests.experiment_data import ExperimentData


class TestFileScanner(unittest.TestCase):
    def setUp(self):
        self.data_folder = fs.DataScanner(ExperimentData.root_path)

    def test_scanner(self):
        self.assertEqual(ExperimentData.root_path + 'beans/preprocessing/20190718/20190718_beans_01_s1.mda',
                         self.data_folder.data['beans']['20190718']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual(len(self.data_folder.data['beans']['20190718']['01_s1'].get_all_data_from_dataset('mda')), 66)
        self.assertEqual(ExperimentData.root_path + 'beans/preprocessing/20190718/20190718_beans_01_s1.time',
                         self.data_folder.data['beans']['20190718']['01_s1'].get_data_path_from_dataset('time'))
