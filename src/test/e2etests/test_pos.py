import unittest

import pandas as pd

from src.datamigration.nwb_builder.pos_extractor import POSExtractor
from .experiment_data import ExperimentData


class TestPOSMigration(unittest.TestCase):

    def setUp(self):
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file

    # def test_reading_pos(self):
    #     pos_extractor = POSExtractor(path=self.path_to_beans)
    #     pos_extractor.get_position()
    #     self.assertEqual((32658, 5), pd.DataFrame(pos_extractor.pos_online['data']).shape, 'Shape should be (32658, 5)')
