from unittest import TestCase
from unittest.mock import Mock

from ndx_franklab_novela import HeaderDevice

from rec_to_nwb.processing.header.module.global_configuration import GlobalConfiguration
from rec_to_nwb.processing.nwb.components.device.device_factory import DeviceFactory
from rec_to_nwb.processing.nwb.components.device.header.fl_header_device_manager import FlHeaderDeviceManager


class TestHeaderDeviceManager(TestCase):
    def test_header_device_manager_create_HeaderDevice_successfully(self):
        mock_configuration = Mock(GlobalConfiguration)
        header_device_manager = FlHeaderDeviceManager("sample_name", mock_configuration, mock_configuration)
        header_device_manager.global_configuration = {
           'headstage_serial': 'Sample headstage_serial',
           'headstage_smart_ref_on': 'Sample headstage_smart_ref_on',
           'realtime_mode': 'Sample realtime_mode',
           'headstage_auto_settle_on': 'Sample headstage_auto_settle_on',
           'timestamp_at_creation': 'Sample timestamp_at_creation',
           'controller_firmware_version': 'Sample controller_firmware_version',
           'controller_serial': 'Sample controller_serial',
           'save_displayed_chan_only': 'Sample save_displayed_chan_only',
           'headstage_firmware_version': 'Sample headstage_firmware_version',
           'qt_version': 'Sample qt_version',
            'compile_date': 'Sample compile_date',
           'compile_time': 'Sample compile_time',
            'file_prefix': 'Sample file_prefix',
           'headstage_gyro_sensor_on': 'Sample headstage_gyro_sensor_on',
           'headstage_mag_sensor_on': 'Sample headstage_mag_sensor_on',
           'trodes_version': 'Sample trodes_version',
           'headstage_accel_sensor_on': 'Sample headstage_accel_sensor_on',
           'commit_head': 'Sample commit_head',
           'system_time_at_creation': 'Sample system_time_at_creation',
           'file_path': 'Sample file_path'
        }
        header_device_manager.default_configuration = {
           'headstage_serial': '1',
           'headstage_smart_ref_on': '1',
           'realtime_mode': '1',
           'headstage_auto_settle_on': '1',
           'timestamp_at_creation': '1',
           'controller_firmware_version': '1',
           'controller_serial': '1',
           'save_displayed_chan_only': '1',
           'headstage_firmware_version': '1',
           'qt_version': '1',
            'compile_date': '1',
           'compile_time': '1',
            'file_prefix': '1',
           'headstage_gyro_sensor_on': '1',
           'headstage_mag_sensor_on': '1',
           'trodes_version': '1',
           'headstage_accel_sensor_on': '1',
           'commit_head': '1',
           'system_time_at_creation': '1',
           'file_path': '1'
        }

        fl_header_device = header_device_manager.get_fl_header_device()
        header_device = DeviceFactory.create_header_device(fl_header_device)

        self.assertIsNotNone(header_device)
        self.assertIsInstance(header_device, HeaderDevice)
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


    def test_header_device_manager_create_HeaderDevice_with_default_values_successfully(self):
        mock_configuration = Mock(GlobalConfiguration)
        header_device_manager = FlHeaderDeviceManager("sample_name", mock_configuration, mock_configuration)
        header_device_manager.global_configuration = {}
        header_device_manager.default_configuration = {
           'headstage_serial': 'Sample headstage_serial',
           'headstage_smart_ref_on': 'Sample headstage_smart_ref_on',
           'realtime_mode': 'Sample realtime_mode',
           'headstage_auto_settle_on': 'Sample headstage_auto_settle_on',
           'timestamp_at_creation': 'Sample timestamp_at_creation',
           'controller_firmware_version': 'Sample controller_firmware_version',
           'controller_serial': 'Sample controller_serial',
           'save_displayed_chan_only': 'Sample save_displayed_chan_only',
           'headstage_firmware_version': 'Sample headstage_firmware_version',
           'qt_version': 'Sample qt_version',
            'compile_date': 'Sample compile_date',
           'compile_time': 'Sample compile_time',
            'file_prefix': 'Sample file_prefix',
           'headstage_gyro_sensor_on': 'Sample headstage_gyro_sensor_on',
           'headstage_mag_sensor_on': 'Sample headstage_mag_sensor_on',
           'trodes_version': 'Sample trodes_version',
           'headstage_accel_sensor_on': 'Sample headstage_accel_sensor_on',
           'commit_head': 'Sample commit_head',
           'system_time_at_creation': 'Sample system_time_at_creation',
           'file_path': 'Sample file_path'
        }

        fl_header_device = header_device_manager.get_fl_header_device()
        header_device = DeviceFactory.create_header_device(fl_header_device)

        self.assertIsNotNone(header_device)
        self.assertIsInstance(header_device, HeaderDevice)
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
