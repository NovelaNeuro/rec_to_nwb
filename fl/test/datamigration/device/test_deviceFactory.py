from unittest import TestCase
from unittest.mock import Mock

from ndx_fllab_novela.header_device import HeaderDevice
from ndx_fllab_novela.probe import Probe
from pynwb.device import Device
from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_in_init_exception import NoneParamInInitException
from fl.datamigration.header.module.global_configuration import GlobalConfiguration
from fl.datamigration.nwb.components.device.device_factory import DeviceFactory
from fl.datamigration.nwb.components.device.fl_device import LfDevice
from fl.datamigration.nwb.components.device.fl_header_device import LfHeaderDevice
from fl.datamigration.nwb.components.device.fl_probe import LfProbe


class TestDeviceFactory(TestCase):

    def test_factory_create_Device_successfully(self):
        mock_fl_device = Mock(spec=LfDevice)
        mock_fl_device.name = 'Device1'
        
        device = DeviceFactory.create_device(
            fl_device=mock_fl_device
        )
        
        self.assertIsNotNone(device)

        self.assertIsInstance(device, Device)
        self.assertEqual(device.name, 'Device1')

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_Device_due_to_none_LfDevice(self):
        DeviceFactory.create_device(
            fl_device=None
        )

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_Device_due_to_none_name_in_LfDevice(self):
        mock_fl_device = Mock(spec=LfDevice)
        mock_fl_device.name = None

        DeviceFactory.create_device(
            fl_device=mock_fl_device
        )

    def test_factory_create_Probe_successfully(self):
        mock_fl_probe = Mock(spec=LfProbe)
        mock_fl_probe.probe_id = 1
        mock_fl_probe.metadata = {
            'probe_type': 'Type1',
            'contact_size': 20.0,
            'num_shanks': 2,
            'contact_side_numbering': True
        }
        
        probe = DeviceFactory.create_probe(
            fl_probe=mock_fl_probe
        )
        
        self.assertIsNotNone(probe)
        self.assertIsInstance(probe, Probe)
        self.assertEqual(probe.name, '1')
        self.assertEqual(probe.id, 1)
        self.assertEqual(probe.num_shanks, 2)
        self.assertEqual(probe.contact_size, 20.0)
        self.assertEqual(probe.probe_type, 'Type1')
        self.assertEqual(probe.contact_side_numbering, True)

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_Probe_due_to_none_LfProbe(self):
        DeviceFactory.create_probe(
            fl_probe=None
        )

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_Probe_due_to_none_param_in_LfProbe(self):
        mock_fl_probe = Mock(spec=LfProbe)
        mock_fl_probe.probe_id = 1
        mock_fl_probe.metadata = None

        DeviceFactory.create_probe(
            fl_probe=mock_fl_probe
        )

    def test_factory_create_HeaderDevice_successfully(self):
        mock_fl_header_device = Mock(spec=LfHeaderDevice)
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
        mock_fl_header_device.name = 'HeaderDevice_1'
        mock_fl_header_device.global_configuration = mock_global_configuration

        header_device = DeviceFactory.create_header_device(
            fl_header_device=mock_fl_header_device
        )
        
        self.assertIsNotNone(header_device)
        self.assertIsInstance(header_device, HeaderDevice)
        self.assertEqual(header_device.name, 'HeaderDevice_1')
        self.assertEqual(header_device.headstage_serial, 'Sample headstage_serial')
        self.assertEqual(header_device.headstage_smart_ref_on, 'Sample headstage_smart_ref_on')
        self.assertEqual(header_device.realtime_mode, 'Sample realtime_mode')
        self.assertEqual(header_device.headstage_auto_settle_on, 'Sample headstage_auto_settle_on')
        self.assertEqual(header_device.timestamp_at_creation, 'Sample timestamp_at_creation')
        self.assertEqual(header_device.controller_firmware_version, 'Sample controller_firmware_version')
        self.assertEqual(header_device.controller_serial, 'Sample controller_serial')
        self.assertEqual(header_device.save_displayed_chan_only, 'Sample save_displayed_chan_only')
        self.assertEqual(header_device.headstage_firmware_version, 'Sample headstage_firmware_version')
        self.assertEqual(header_device.qt_version, 'Sample qt_version')
        self.assertEqual(header_device.compile_date, 'Sample compile_date')
        self.assertEqual(header_device.compile_time, 'Sample compile_time')
        self.assertEqual(header_device.file_prefix, 'Sample file_prefix')
        self.assertEqual(header_device.headstage_gyro_sensor_on, 'Sample headstage_gyro_sensor_on')
        self.assertEqual(header_device.headstage_mag_sensor_on, 'Sample headstage_mag_sensor_on')
        self.assertEqual(header_device.trodes_version, 'Sample trodes_version')
        self.assertEqual(header_device.headstage_accel_sensor_on, 'Sample headstage_accel_sensor_on')
        self.assertEqual(header_device.commit_head, 'Sample commit_head')
        self.assertEqual(header_device.system_time_at_creation, 'Sample system_time_at_creation')
        self.assertEqual(header_device.file_path, 'Sample file_path')

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_HeaderDevice_due_to_none_LfHeaderDevice(self):
        DeviceFactory.create_header_device(
            fl_header_device=None
        )

    @should_raise(NoneParamInInitException)
    def test_factory_failed_creating_Probe_due_to_none_param_in_LfProbe(self):
        mock_fl_header_device = Mock(spec=LfHeaderDevice)
        mock_fl_header_device.name = 'HeaderDevice_1'
        mock_fl_header_device.global_configuration = None

        DeviceFactory.create_header_device(
            fl_header_device=mock_fl_header_device
        )