import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile


class TestTravis(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(session_description='demonstrate external files',
                                identifier='NWBE1',
                                session_start_time=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
                                )

    def test_travis(self):
        self.assertIsNotNone(self.nwb_file)
