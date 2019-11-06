import os
import unittest

from mountainlab_pytools.mdaio import readmda

from experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.ntrode = readmda(ExperimentData.mda_path + ExperimentData.mda_file)
        self.timestamps = readmda(ExperimentData.mda_path + ExperimentData.mda_timestamp)

        mda_files = [mda_file for mda_file in os.listdir(ExperimentData.mda_path) if
                     (mda_file.endswith('.mda') and mda_file != ExperimentData.mda_timestamp)]
        print(mda_files)

    def test_reading_mda(self):
        self.assertIsNotNone(self.timestamps)
        self.assertIsNotNone(self.ntrode)
        self.assertEqual(self.timestamps.shape, (21839001,), 'Should be (21839001,)')
        self.assertEqual(self.ntrode.shape, (4, 21839001), 'Should be (4, 21839001)')
