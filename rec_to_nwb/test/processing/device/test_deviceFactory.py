from unittest import TestCase
from unittest.mock import Mock
from testfixtures import should_raise

from ndx_franklab_novela.header_device import HeaderDevice
from ndx_franklab_novela.probe import Probe, Shank
from pynwb.device import Device

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.header.module.global_configuration import GlobalConfiguration
from rec_to_nwb.processing.nwb.components.device.device_factory import DeviceFactory
from rec_to_nwb.processing.nwb.components.device.fl_device import FlDevice
from rec_to_nwb.processing.nwb.components.device.fl_header_device import FlHeaderDevice
from rec_to_nwb.processing.nwb.components.device.fl_probe import FlProbe


class TestDeviceFactory(TestCase):

    def test_factory_create_Device_successfully(self):
        mock_fl_device = Mock(spec=FlDevice)
        mock_fl_device.name = 'Device1'
        
        device = DeviceFactory.create_device(
            fl_device=mock_fl_device
        )
        
        self.assertIsNotNone(device)

        self.assertIsInstance(device, Device)
        self.assertEqual(device.name, 'Device1')

    @should_raise(TypeError)
    def test_factory_failed_creating_Device_due_to_none_FlDevice(self):
        DeviceFactory.create_device(
            fl_device=None
        )

    @should_raise(NoneParamException)
    def test_factory_failed_creating_Device_due_to_none_name_in_FlDevice(self):
        mock_fl_device = Mock(spec=FlDevice)
        mock_fl_device.name = None

        DeviceFactory.create_device(
            fl_device=mock_fl_device
        )

    def test_factory_create_Probe_successfully(self):
        mock_shank_1 = Mock(spec=Shank)
        mock_shank_2 = Mock(spec=Shank)

        mock_fl_probe = Mock(spec=FlProbe)
        mock_fl_probe.probe_id = 1
        mock_fl_probe.name = 'probe 1'
        mock_fl_probe.probe_type = 'Type1'
        mock_fl_probe.units = 'um'
        mock_fl_probe.probe_description = 'sample description'
        mock_fl_probe.contact_side_numbering = True
        mock_fl_probe.contact_size = 20.0
        mock_fl_probe.shanks = [mock_shank_1, mock_shank_2]
        
        probe = DeviceFactory.create_probe(
            fl_probe=mock_fl_probe
        )
        
        self.assertIsNotNone(probe)
        self.assertIsInstance(probe, Probe)

        self.assertEqual(probe.name, 'probe 1')
        self.assertEqual(probe.id, 1)
        self.assertEqual(probe.contact_size, 20.0)
        self.assertEqual(probe.probe_type, 'Type1')
        self.assertEqual(probe.units, 'um')
        self.assertEqual(probe.probe_description, 'sample description')
        self.assertEqual(probe.contact_side_numbering, True)
        self.assertEqual(probe.shanks, {
            mock_shank_1.name: mock_shank_1,
            mock_shank_2.name: mock_shank_2
        })

    @should_raise(TypeError)
    def test_factory_failed_creating_Probe_due_to_none_FlProbe(self):
        DeviceFactory.create_probe(
            fl_probe=None
        )

    @should_raise(NoneParamException)
    def test_factory_failed_creating_Probe_due_to_none_param_in_metadata_FlProbe(self):
        mock_fl_probe = Mock(spec=FlProbe)
        mock_fl_probe.probe_id = 1
        mock_fl_probe.name = None
        mock_fl_probe.probe_type = None
        mock_fl_probe.units = None
        mock_fl_probe.probe_description = None
        mock_fl_probe.contact_side_numbering = None
        mock_fl_probe.contact_size = None
        mock_fl_probe.shanks = None

        DeviceFactory.create_probe(
            fl_probe=mock_fl_probe
        )

    def test_factory_create_HeaderDevice_successfully(self):
        mock_fl_header_device = Mock(spec=FlHeaderDevice)
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

    @should_raise(TypeError)
    def test_factory_failed_creating_HeaderDevice_due_to_none_FlHeaderDevice(self):
        DeviceFactory.create_header_device(
            fl_header_device=None
        )

    @should_raise(NoneParamException)
    def test_factory_failed_creating_Probe_due_to_none_param_in_FlProbe(self):
        mock_fl_header_device = Mock(spec=FlHeaderDevice)
        mock_fl_header_device.name = 'HeaderDevice_1'
        mock_fl_header_device.global_configuration = None

        DeviceFactory.create_header_device(
            fl_header_device=mock_fl_header_device
        )