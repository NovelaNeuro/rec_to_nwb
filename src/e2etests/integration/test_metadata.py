import os
import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb.epoch import TimeIntervals

from src.datamigration.nwb_file_creator import NWBFileCreator


class TestMetadata(unittest.TestCase):

    def setUp(self):
        nwb_builder = NWBFileCreator('John the experimenter',
                                     'novela lab', 'novela institution',
                                     'our novela experiment',
                                     'description of the novela session',
                                     datetime(2019, 10, 31, tzinfo=tzlocal()),
                                     'some novela indentifier'
                                     )
        nwb_builder.build()

    def test_building_nwb(self):
        self.assertNotEqual(0, os.path.getsize('example_file_path.nwb'))

    def test_write_task(self):
        task = TimeIntervals("testName", description="testDescription", id=None, columns=None, colnames=None)
        task.add_interval(1.0, 10.0, tags=None, timeseries=None)

        self.assertEqual(isinstance(task, TimeIntervals), True, 'task should be instance of TimeIntervals')
        self.assertEqual(task.__getitem__('start_time')[0:1][0], 1.0, 'start_time value should be (1.0)')
