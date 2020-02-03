import logging.config
import os
from datetime import datetime
from unittest import TestCase

from dateutil.tz import tzlocal
from pynwb import NWBFile

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup
from src.datamigration.extension.ntrode import NTrode
from src.datamigration.extension.probe import Probe

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=path + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class TestExtensions(TestCase):

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
            id=1,
            probe_type='some type',
            contact_size=20.0,
            num_shanks=2,
        )
        cls.nwb_file.add_device(cls.probe)

        cls.fl_electrode_group = FLElectrodeGroup(
            name='FLElectrodeGroup1',
            description='sample description',
            location='sample location',
            device=cls.probe,
            id=1,
        )
        cls.nwb_file.add_electrode_group(cls.fl_electrode_group)

        cls.n_trode = NTrode(
            name='NTrode1',
            description='sample description',
            location='sample location',
            device=cls.probe,
            probe_id=1,
            ntrode_id=1,
            map=[[0, 0], [1, 1], [2, 2]]
        )
        cls.nwb_file.add_electrode_group(cls.n_trode)

    def test_probe_creation(self):
        return_probe = self.nwb_file.get_device(name='Probe1')

        self.assertEqual(self.probe, return_probe)
        self.assertEqual(self.probe.name, return_probe.name)
        self.assertEqual(self.probe.id, return_probe.id)
        self.assertEqual(self.probe.contact_size, return_probe.contact_size)
        self.assertEqual(self.probe.num_shanks, return_probe.num_shanks)

    def test_fl_electrode_group_creation(self):
        return_fl_electrode_group = self.nwb_file.get_electrode_group(name='FLElectrodeGroup1')

        self.assertEqual(self.fl_electrode_group, return_fl_electrode_group)
        self.assertEqual(self.fl_electrode_group.name, return_fl_electrode_group.name)
        self.assertEqual(self.fl_electrode_group.description, return_fl_electrode_group.description)
        self.assertEqual(self.fl_electrode_group.location, return_fl_electrode_group.location)
        self.assertEqual(self.fl_electrode_group.device, return_fl_electrode_group.device)
        self.assertEqual(self.fl_electrode_group.id, return_fl_electrode_group.id)

    def test_n_trode_creation(self):
        return_n_trode = self.nwb_file.get_electrode_group(name='NTrode1')

        self.assertEqual(self.n_trode, return_n_trode)
        self.assertEqual(self.n_trode.name, return_n_trode.name)
        self.assertEqual(self.n_trode.description, return_n_trode.description)
        self.assertEqual(self.n_trode.location, return_n_trode.location)
        self.assertEqual(self.n_trode.device, return_n_trode.device)
        self.assertEqual(self.n_trode.probe_id, return_n_trode.probe_id)
        self.assertEqual(self.n_trode.ntrode_id, return_n_trode.ntrode_id)
        self.assertEqual(self.n_trode.map, return_n_trode.map)
