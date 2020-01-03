import unittest
from datetime import datetime

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.extension.probe import Probe


class TestExtensions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nwb_file = NWBFile(
            session_description='demonstrate external files',
            identifier='NWBE1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        cls.probe = Probe(
            name='Probe1',
            device_name='Device1',
            probe_description='Sample description'
        )
        cls.nwb_file.add_device(cls.probe)

    def test_probe_creation(self):
        return_probe = self.nwb_file.get_device(name='Probe1')
        self.assertEqual(self.probe, return_probe)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.device_name, return_probe.device_name)
        self.assertEqual(self.probe.probe_description, return_probe.probe_description)
