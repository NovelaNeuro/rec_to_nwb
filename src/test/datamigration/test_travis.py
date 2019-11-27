import datetime
import unittest

import dateutil
from pynwb import NWBFile

start_time = datetime.time(1, 2, tzinfo=dateutil.tz.UTC)


class TestTravis(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(session_description='demonstrate external files',
                                identifier='NWBE1',
                                session_start_time=start_time
                                )



    def test_travis(self):
        self.assertIsNotNone(self.nwb_file)
        self.assertIsInstance(start_time, datetime)
