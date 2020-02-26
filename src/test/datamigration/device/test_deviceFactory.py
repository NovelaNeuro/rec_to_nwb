from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela.header_device import HeaderDevice
from ndx_franklab_novela.probe import Probe
from pynwb.device import Device

from src.datamigration.header.module.global_configuration import GlobalConfiguration
from src.datamigration.nwb.components.device.device_factory import DeviceFactory
from src.datamigration.nwb.components.device.lf_device import LfDevice
from src.datamigration.nwb.components.device.lf_header_device import LfHeaderDevice
from src.datamigration.nwb.components.device.lf_probe import LfProbe


class TestDeviceFactory(TestCase):

    @classmethod
    def setUpClass(cls):

        mock_lf_device = Mock(spec=LfDevice)
        mock_lf_device.name = 'Device1'

        mock_lf_probe = Mock(spec=LfProbe)
        mock_lf_probe.metadata = {
            'probe_type': 'Type1',
            'contact_size': 20.0,
            'num_shanks': 2
        }
        mock_lf_probe.probe_id = 1

        mock_lf_header_device = Mock(spec=LfHeaderDevice)
        mock_global_configuration = Mock(spec=GlobalConfiguration)
        mock_global_configuration.headstage_serial = 'Sample headstage_serial'
        mock_global_configuration.headstage_smart_ref_on = 'Sample headstage_smart_ref_on'
        mock_global_configuration.realtime_mode = 'Sample realtime_mode'
        mock_global_configuration.headstage_auto_settle_on = 'Sample headstage_auto_settle_on'
        mock_global_configuration.timestamp_at_creation = 'Sample timestamp_at_creation'
        mock_global_configuration.controller_firmware_version = 'Sample controller_firmware_version'
        mock_global_configuration.controller_serial = 'Sample controller_serial'
        mock_global_configuration.save_displayed_chan_only = 'Sample save_displayed_chan_only'
        mock_global_configuration.headstage_firmware_version = 'Sample headstage_firmware_version'
        mock_global_configuration.qt_version = 'Sample qt_version'
        mock_global_configuration.compile_date = 'Sample compile_date'
        mock_global_configuration.compile_time = 'Sample compile_time'
        mock_global_configuration.file_prefix = 'Sample file_prefix'
        mock_global_configuration.headstage_gyro_sensor_on = 'Sample headstage_gyro_sensor_on'
        mock_global_configuration.headstage_mag_sensor_on = 'Sample headstage_mag_sensor_on'
        mock_global_configuration.trodes_version = 'Sample trodes_version'
        mock_global_configuration.headstage_accel_sensor_on = 'Sample headstage_accel_sensor_on'
        mock_global_configuration.commit_head = 'Sample commit_head'
        mock_global_configuration.system_time_at_creation = 'Sample system_time_at_creation'
        mock_global_configuration.file_path = 'Sample file_path'
        mock_lf_header_device.name ='HeaderDevice1'
        mock_lf_header_device.global_configuration = mock_global_configuration

        cls.device = DeviceFactory.create_device(
            lf_device=mock_lf_device
        )

        cls.probe = DeviceFactory.create_probe(
            lf_probe=mock_lf_probe
        )

        cls.header_device = DeviceFactory.create_header_device(
            lf_header_device=mock_lf_header_device
        )

    def test_createDevice_successfulCreate_true(self):
        self.assertIsNotNone(self.device)

    def test_createDevice_containCorrectType_true(self):
        self.assertIsInstance(self.device, Device)

        self.assertIsInstance(self.device.name, str)

    def test_createDevice_containCorrectValues_true(self):
        self.assertEqual(self.device.name, 'Device1')

    def test_createProbe_successfulCreate_true(self):
        self.assertIsNotNone(self.probe)

    def test_createProbe_containCorrectType_true(self):
        self.assertIsInstance(self.probe, Probe)

        self.assertIsInstance(self.probe.name, str)

    def test_createProbe_containCorrectValues_true(self):
        self.assertEqual(self.probe.name, '1')
        self.assertEqual(self.probe.id, 1)
        self.assertEqual(self.probe.num_shanks, 2)
        self.assertEqual(self.probe.contact_size, 20.0)
        self.assertEqual(self.probe.probe_type, 'Type1')

    def test_createHeaderDevice_successfulCreate_true(self):
        self.assertIsNotNone(self.header_device)

    def test_createHeaderDevice_containCorrectType_true(self):
        self.assertIsInstance(self.header_device, HeaderDevice)

        self.assertIsInstance(self.header_device.headstage_serial, str)
        self.assertIsInstance(self.header_device.headstage_smart_ref_on, str)
        self.assertIsInstance(self.header_device.realtime_mode, str)
        self.assertIsInstance(self.header_device.headstage_auto_settle_on, str)
        self.assertIsInstance(self.header_device.timestamp_at_creation, str)
        self.assertIsInstance(self.header_device.controller_firmware_version, str)
        self.assertIsInstance(self.header_device.controller_serial, str)
        self.assertIsInstance(self.header_device.save_displayed_chan_only, str)
        self.assertIsInstance(self.header_device.headstage_firmware_version, str)
        self.assertIsInstance(self.header_device.qt_version, str)
        self.assertIsInstance(self.header_device.compile_date, str)
        self.assertIsInstance(self.header_device.compile_time, str)
        self.assertIsInstance(self.header_device.file_prefix, str)
        self.assertIsInstance(self.header_device.headstage_gyro_sensor_on, str)
        self.assertIsInstance(self.header_device.headstage_mag_sensor_on, str)
        self.assertIsInstance(self.header_device.trodes_version, str)
        self.assertIsInstance(self.header_device.headstage_accel_sensor_on, str)
        self.assertIsInstance(self.header_device.commit_head, str)
        self.assertIsInstance(self.header_device.system_time_at_creation, str)
        self.assertIsInstance(self.header_device.file_path, str)

    def test_createHeaderDevice_containCorrectValues_true(self):
        self.assertEqual(self.header_device.name, 'HeaderDevice1')
        self.assertEqual(self.header_device.headstage_serial, 'Sample headstage_serial')
        self.assertEqual(self.header_device.headstage_smart_ref_on, 'Sample headstage_smart_ref_on')
        self.assertEqual(self.header_device.realtime_mode, 'Sample realtime_mode')
        self.assertEqual(self.header_device.headstage_auto_settle_on, 'Sample headstage_auto_settle_on')
        self.assertEqual(self.header_device.timestamp_at_creation, 'Sample timestamp_at_creation')
        self.assertEqual(self.header_device.controller_firmware_version, 'Sample controller_firmware_version')
        self.assertEqual(self.header_device.controller_serial, 'Sample controller_serial')
        self.assertEqual(self.header_device.save_displayed_chan_only, 'Sample save_displayed_chan_only')
        self.assertEqual(self.header_device.headstage_firmware_version, 'Sample headstage_firmware_version')
        self.assertEqual(self.header_device.qt_version, 'Sample qt_version')
        self.assertEqual(self.header_device.compile_date, 'Sample compile_date')
        self.assertEqual(self.header_device.compile_time, 'Sample compile_time')
        self.assertEqual(self.header_device.file_prefix, 'Sample file_prefix')
        self.assertEqual(self.header_device.headstage_gyro_sensor_on, 'Sample headstage_gyro_sensor_on')
        self.assertEqual(self.header_device.headstage_mag_sensor_on, 'Sample headstage_mag_sensor_on')
        self.assertEqual(self.header_device.trodes_version, 'Sample trodes_version')
        self.assertEqual(self.header_device.headstage_accel_sensor_on, 'Sample headstage_accel_sensor_on')
        self.assertEqual(self.header_device.commit_head, 'Sample commit_head')
        self.assertEqual(self.header_device.system_time_at_creation, 'Sample system_time_at_creation')
        self.assertEqual(self.header_device.file_path, 'Sample file_path')
