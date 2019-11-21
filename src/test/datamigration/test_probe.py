from datetime import datetime
from unittest import TestCase

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.fl_probe import Probe


class TestProbe(TestCase):

    def setUp(self):
        start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
        create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        self.nwbfile = NWBFile('', '1', start_time,
                               file_create_date=create_date)

    def test_configuration_tag(self):
        probe = Probe(name='Probe1', Probe_name='aaa')
        self.nwbfile.add_device(probe)

        return_probe = self.nwbfile.get_device(name='Probe1')
        self.assertEqual(probe, return_probe)
        self.assertEqual(probe.name, return_probe.name)
        self.assertEqual(probe.Probe_name, return_probe.Probe_name)
