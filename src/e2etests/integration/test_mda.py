import unittest

from mountainlab_pytools.mdaio import readmda

from experiment_data import ExperimentData


class TestMDAMigration(unittest.TestCase):

    def setUp(self):
        print('Test requires preprocessed test_data folder at e2etests location')
        self.timestamps = readmda(ExperimentData.mda_path + ExperimentData.mda_file)
        self.ntrode = readmda(ExperimentData.mda_path + ExperimentData.mda_timestamp)

    def test_reading_mda(self):
        self.assertIsNotNone(self.timestamps)
        self.assertIsNotNone(self.ntrode)
        self.assertEqual(self.ntrode.shape, (21839001,), 'Should be (21839001,)')
        self.assertEqual(self.timestamps.shape, (4, 21839001), 'Should be (4, 21839001)')
