from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from ndx_fl_novela.header_device import HeaderDevice
from ndx_fl_novela.probe import Probe
from pynwb import NWBFile
from pynwb.device import Device
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.device.device_injector import DeviceInjector


class TestDeviceInjector(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.header_device_1 = Mock(spec=HeaderDevice)
        cls.header_device_1.name = 'HeaderDevice_1'
        cls.header_device_1.headstage_serial = 'Sample headstage_serial'
        cls.header_device_1.headstage_smart_ref_on = 'Sample headstage_smart_ref_on'
        cls.header_device_1.realtime_mode = 'Sample realtime_mode'
        cls.header_device_1.headstage_auto_settle_on = 'Sample headstage_auto_settle_on'
        cls.header_device_1.timestamp_at_creation = 'Sample timestamp_at_creation'
        cls.header_device_1.controller_firmware_version = 'Sample controller_firmware_version'
        cls.header_device_1.controller_serial = 'Sample controller_serial'
        cls.header_device_1.save_displayed_chan_only = 'Sample save_displayed_chan_only'
        cls.header_device_1.headstage_firmware_version = 'Sample headstage_firmware_version'
        cls.header_device_1.qt_version = 'Sample qt_version'
        cls.header_device_1.compile_date = 'Sample compile_date'
        cls.header_device_1.compile_time = 'Sample compile_time'
        cls.header_device_1.file_prefix = 'Sample file_prefix'
        cls.header_device_1.headstage_gyro_sensor_on = 'Sample headstage_gyro_sensor_on'
        cls.header_device_1.headstage_mag_sensor_on = 'Sample headstage_mag_sensor_on'
        cls.header_device_1.trodes_version = 'Sample trodes_version'
        cls.header_device_1.headstage_accel_sensor_on = 'Sample headstage_accel_sensor_on'
        cls.header_device_1.commit_head = 'Sample commit_head'
        cls.header_device_1.system_time_at_creation = 'Sample system_time_at_creation'
        cls.header_device_1.file_path = 'Sample file_path'

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

        cls.device_1 = Mock(spec=Device)
        cls.device_1.name = 'Device_1'

        cls.device_2 = Mock(spec=Device)
        cls.device_2.name = 'Device_2'

        cls.probes_dict = {'Probe_1': cls.probe_1, 'Probe_2': cls.probe_2}

        cls.header_device_dict = {'HeaderDevice_1': cls.header_device_1}

        cls.device_dict = {'Device_1': cls.device_1, 'Device_2': cls.device_2}

        cls.device_injector = DeviceInjector()

    def setUp(self):
        self.nwb_content = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

    def test_injector_inject_device_to_nwb_successfully(self):
        self.device_injector.inject_all_devices(
            nwb_content=self.nwb_content,
            devices=[self.device_1, self.device_2]
        )

        self.assertEqual(self.nwb_content.devices, self.device_dict)
        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertIsInstance(self.nwb_content.devices['Device_1'], Device)
        self.assertEqual(self.nwb_content.devices['Device_1'].name, 'Device_1')

        self.assertIsInstance(self.nwb_content.devices['Device_2'], Device)
        self.assertEqual(self.nwb_content.devices['Device_2'].name, 'Device_2')

    def test_injector_inject_probes_to_nwb_successfully(self):
        self.device_injector.inject_all_devices(
            nwb_content=self.nwb_content,
            devices=[self.probe_1, self.probe_2]
        )

        self.assertEqual(self.nwb_content.devices, self.probes_dict)
        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertIsInstance(self.nwb_content.devices['Probe_1'], Probe)
        self.assertEqual(self.nwb_content.devices['Probe_1'].id, 1)
        self.assertEqual(self.nwb_content.devices['Probe_1'].name, 'Probe_1')
        self.assertEqual(self.nwb_content.devices['Probe_1'].num_shanks, 20)
        self.assertEqual(self.nwb_content.devices['Probe_1'].contact_size, 20.0)

        self.assertIsInstance(self.nwb_content.devices['Probe_2'], Probe)
        self.assertEqual(self.nwb_content.devices['Probe_2'].id, 2)
        self.assertEqual(self.nwb_content.devices['Probe_2'].name, 'Probe_2')
        self.assertEqual(self.nwb_content.devices['Probe_2'].num_shanks, 30)
        self.assertEqual(self.nwb_content.devices['Probe_2'].contact_size, 25.0)

    def test_injector_inject_header_device_to_nwb_successfully(self):
        self.device_injector.inject_all_devices(
            nwb_content=self.nwb_content,
            devices=[self.header_device_1]
        )

        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].name, 'HeaderDevice_1')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_serial, 'Sample headstage_serial')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_smart_ref_on,
                         'Sample headstage_smart_ref_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].realtime_mode, 'Sample realtime_mode')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_auto_settle_on,
                         'Sample headstage_auto_settle_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].timestamp_at_creation,
                         'Sample timestamp_at_creation')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].controller_firmware_version,
                         'Sample controller_firmware_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].controller_serial, 'Sample controller_serial')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].save_displayed_chan_only,
                         'Sample save_displayed_chan_only')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_firmware_version,
                         'Sample headstage_firmware_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].qt_version, 'Sample qt_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].compile_date, 'Sample compile_date')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].compile_time, 'Sample compile_time')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].file_prefix, 'Sample file_prefix')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_gyro_sensor_on,
                         'Sample headstage_gyro_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_mag_sensor_on,
                         'Sample headstage_mag_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].trodes_version, 'Sample trodes_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].headstage_accel_sensor_on,
                         'Sample headstage_accel_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].commit_head, 'Sample commit_head')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].system_time_at_creation,
                         'Sample system_time_at_creation')
        self.assertEqual(self.nwb_content.devices['HeaderDevice_1'].file_path, 'Sample file_path')

    @should_raise(NoneParamException)
    def test_injector_failed_injecting_devices_to_nwb_due_to_None_devices(self):
        self.device_injector.inject_all_devices(
            nwb_content=self.nwb_content,
            devices=None
        )

    @should_raise(NoneParamException)
    def test_injector_failed_injecting_devices_to_nwb_due_to_None_nwb(self):
        self.device_injector.inject_all_devices(
            nwb_content=None,
            devices=[self.probe_1, self.probe_2]
        )
