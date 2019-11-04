import unittest

import pandas as pd
from experiment_data import ExperimentData
from pynwb.behavior import Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class TestPOSMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file
        self.pos_online = readTrodesExtractedDataFile(self.path_to_beans)

    def test_reading_pos(self):
        position_online = pd.DataFrame(self.pos_online['data'])
        position = Position()
        position.create_spatial_series(
            name="TestName",
            data=(position_online.xloc, position_online.yloc, position_online.xloc2, position_online.yloc2),
            # What should be inside this field?
            reference_frame="Description defining what the zero-position is",
            timestamps=position_online.time.tolist()
        )
        self.assertEqual(position_online.shape, (32658, 5), 'Shape should be (32658, 5)')
