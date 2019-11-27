import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

start_time = datetime(2017, 4, 3, tzinfo=tzlocal())
create_date = datetime(2017, 4, 12, tzinfo=tzlocal())


class TestTravis(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(session_description='demonstrate external files',
                           identifier='NWBE1',
                           session_start_time=start_time,
                           file_create_date=create_date)


    def test_travis(self):
       self.assertIsNotNone(self.nwb_file)
