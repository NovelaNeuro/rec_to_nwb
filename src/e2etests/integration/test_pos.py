import unittest

import pandas as pd
from experiment_data import ExperimentData

from src.datamigration.nwb.pos_extractor import POSExtractor


class TestPOSMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file

    def test_reading_pos(self):
        pos_extractor = POSExtractor(
            path=self.path_to_beans)
        position = pos_extractor.get_position()
        self.assertEqual((32658, 5), pd.DataFrame(pos_extractor.pos_online['data']).shape, 'Shape should be (32658, 5)')
