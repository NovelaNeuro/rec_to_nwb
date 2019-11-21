from datetime import datetime
from unittest import TestCase

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.extension.fl_probe import Probe
from src.datamigration.extension.fl_shank import Shank


class TestProbe(TestCase):

    def setUp(self):
        start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())
        create_date = datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        self.nwbfile = NWBFile('', '1', start_time,
                               file_create_date=create_date)
        self.probe = Probe(name='Probe1', Probe_name='aaa')

    def test_probe_creation(self):
        self.probe = Probe(name='Probe1', Probe_name='aaa')
        self.nwbfile.add_device(self.probe)

        return_probe = self.nwbfile.get_device(name='Probe1')
        self.assertEqual(self.probe, return_probe)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.Probe_name, return_probe.Probe_name)

    def test_shank_creation(self):
        self.nwbfile.add_electrode_group(Shank(
                                                Shank_name='some shank name',
                                                name='regular eg name',
                                                description='shank desc', location='xyzshank', device=self.probe))

        self.nwbfile.add_electrode_group(Shank(
            Shank_name='some shank namew',
            name='regular eg namew',
            description='shank descw', location='xyzshankw', device=self.probe))

        print(self.nwbfile.electrode_groups)

