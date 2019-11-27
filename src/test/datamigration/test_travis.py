import unittest
from datetime import datetime

from pynwb import NWBFile

# start_time = datetime.date(1)
timestamp = 1545730073
dt_object = datetime.fromtimestamp(timestamp)


class TestTravis(unittest.TestCase):

    def setUp(self):
        self.nwb_file = NWBFile(session_description='demonstrate external files',
                                identifier='NWBE1',
                                session_start_time=None
                                )

    def test_travis(self):
        self.assertIsNotNone(self.nwb_file)
