from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from ndx_franklab_novela.probe import Probe
from pynwb import NWBFile

from src.datamigration.nwb.components.device.probe_injector import ProbeInjector


class TestProbeInjector(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.probe_1 = Mock(spec=Probe)
        cls.probe_1.name = 'Probe_1'
        cls.probe_1.probe_type = 'type_1'
        cls.probe_1.id = 1
        cls.probe_1.contact_size = 20.0
        cls.probe_1.num_shanks = 20

        cls.probe_2 = Mock(spec=Probe)
        cls.probe_2.name = 'Probe_2'
        cls.probe_2.probe_type = 'type_2'
        cls.probe_2.id = 2
        cls.probe_2.contact_size = 25.0
        cls.probe_2.num_shanks = 30

        cls.probes_dict = {'Probe_1': cls.probe_1, 'Probe_2': cls.probe_2}

        cls.probe_injector = ProbeInjector()

    def setUp(self):
        self.nwb_content = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

    def test_injectAllProbes_correctValuesInjected_true(self):
        self.probe_injector.inject_all_probes(
            nwb_content=self.nwb_content,
            probes=self.probes_dict
        )

        self.assertEqual(self.nwb_content.devices, self.probes_dict)

        self.assertEqual(self.nwb_content.devices['Probe_1'].id, 1)
        self.assertEqual(self.nwb_content.devices['Probe_1'].name, 'Probe_1')
        self.assertEqual(self.nwb_content.devices['Probe_1'].num_shanks, 20)
        self.assertEqual(self.nwb_content.devices['Probe_1'].contact_size, 20.0)

        self.assertEqual(self.nwb_content.devices['Probe_2'].id, 2)
        self.assertEqual(self.nwb_content.devices['Probe_2'].name, 'Probe_2')
        self.assertEqual(self.nwb_content.devices['Probe_2'].num_shanks, 30)
        self.assertEqual(self.nwb_content.devices['Probe_2'].contact_size, 25.0)

    def test_injectAllProbes_correctTypesInjected_true(self):
        self.probe_injector.inject_all_probes(
            nwb_content=self.nwb_content,
            probes=self.probes_dict
        )

        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertIsInstance(self.nwb_content.devices['Probe_1'], Probe)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].id, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].name, str)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].num_shanks, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].contact_size, float)

        self.assertIsInstance(self.nwb_content.devices['Probe_2'], Probe)
        self.assertIsInstance(self.nwb_content.devices['Probe_2'].id, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_2'].name, str)
        self.assertIsInstance(self.nwb_content.devices['Probe_2'].num_shanks, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_2'].contact_size, float)

    def test_injectProbe_correctTypeInjected_true(self):
        self.probe_injector.inject_probe(
            nwb_content=self.nwb_content,
            probe=self.probe_1
        )

        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertIsInstance(self.nwb_content.devices['Probe_1'], Probe)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].id, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].name, str)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].num_shanks, int)
        self.assertIsInstance(self.nwb_content.devices['Probe_1'].contact_size, float)

    def test_injectProbe_correctValuesInjected_true(self):
        self.probe_injector.inject_probe(
            nwb_content=self.nwb_content,
            probe=self.probe_1
        )

        self.assertEqual(self.nwb_content.devices, {'Probe_1': self.probe_1})

        self.assertEqual(self.nwb_content.devices['Probe_1'].id, 1)
        self.assertEqual(self.nwb_content.devices['Probe_1'].name, 'Probe_1')
        self.assertEqual(self.nwb_content.devices['Probe_1'].num_shanks, 20)
        self.assertEqual(self.nwb_content.devices['Probe_1'].contact_size, 20.0)
