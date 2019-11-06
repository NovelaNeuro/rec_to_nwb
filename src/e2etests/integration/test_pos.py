import unittest

import pandas as pd
from pynwb.behavior import SpatialSeries, Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from experiment_data import ExperimentData


class TestPOSMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file
        self.pos_online = readTrodesExtractedDataFile(self.path_to_beans)

    def test_reading_pos(self):
        position_online = pd.DataFrame(self.pos_online['data'])

        series = SpatialSeries(
            name="TestName",
            data=(position_online.xloc, position_online.yloc, position_online.xloc2, position_online.yloc2),
            # What should be inside this field?
            reference_frame="Description defining what the zero-position is",
            timestamps=position_online.time.tolist()
        )
        position = Position(spatial_series=series)
        self.assertEqual(position_online.shape, (32658, 5), 'Shape should be (32658, 5)')

        print(position)  # added just to avoid pylint warnings about unused position
