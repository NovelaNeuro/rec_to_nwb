from datetime import datetime
from unittest import TestCase
from unittest.mock import Mock

from dateutil.tz import tzlocal
from ndx_franklab_novela.header_device import HeaderDevice
from pynwb import NWBFile

from src.datamigration.nwb.components.device.header_device_injector import HeaderDeviceInjector


class TestHeaderDeviceInjector(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.header_device = Mock(spec=HeaderDevice)
        cls.header_device.name = 'HeaderDevice1'
        cls.header_device.headstage_serial = 'Sample headstage_serial'
        cls.header_device.headstage_smart_ref_on = 'Sample headstage_smart_ref_on'
        cls.header_device.realtime_mode = 'Sample realtime_mode'
        cls.header_device.headstage_auto_settle_on = 'Sample headstage_auto_settle_on'
        cls.header_device.timestamp_at_creation = 'Sample timestamp_at_creation'
        cls.header_device.controller_firmware_version = 'Sample controller_firmware_version'
        cls.header_device.controller_serial = 'Sample controller_serial'
        cls.header_device.save_displayed_chan_only = 'Sample save_displayed_chan_only'
        cls.header_device.headstage_firmware_version = 'Sample headstage_firmware_version'
        cls.header_device.qt_version = 'Sample qt_version'
        cls.header_device.compile_date = 'Sample compile_date'
        cls.header_device.compile_time = 'Sample compile_time'
        cls.header_device.file_prefix = 'Sample file_prefix'
        cls.header_device.headstage_gyro_sensor_on = 'Sample headstage_gyro_sensor_on'
        cls.header_device.headstage_mag_sensor_on = 'Sample headstage_mag_sensor_on'
        cls.header_device.trodes_version = 'Sample trodes_version'
        cls.header_device.headstage_accel_sensor_on = 'Sample headstage_accel_sensor_on'
        cls.header_device.commit_head = 'Sample commit_head'
        cls.header_device.system_time_at_creation = 'Sample system_time_at_creation'
        cls.header_device.file_path = 'Sample file_path'

        cls.devices_dict = {'HeaderDevice1': cls.header_device}

        cls.header_device_injector = HeaderDeviceInjector()
        cls.nwb_content = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

        cls.header_device_injector.inject_header_device(
            nwb_content=cls.nwb_content,
            header_device=cls.header_device
        )

    def test_injectHeaderDevice_correctTypeInjected_true(self):
        self.assertIsInstance(self.nwb_content.devices, dict)

        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_serial, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_smart_ref_on, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].realtime_mode, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_auto_settle_on, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].timestamp_at_creation, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].controller_firmware_version, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].controller_serial, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].save_displayed_chan_only, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_firmware_version, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].qt_version, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].compile_date, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].compile_time, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].file_prefix, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_gyro_sensor_on, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_mag_sensor_on, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].trodes_version, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].headstage_accel_sensor_on, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].commit_head, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].system_time_at_creation, str)
        self.assertIsInstance(self.nwb_content.devices['HeaderDevice1'].file_path, str)

    def test_injectHeaderDevice_correctValuesInjected_true(self):
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].name, 'HeaderDevice1')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_serial, 'Sample headstage_serial')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_smart_ref_on,
                         'Sample headstage_smart_ref_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].realtime_mode, 'Sample realtime_mode')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_auto_settle_on,
                         'Sample headstage_auto_settle_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].timestamp_at_creation,
                         'Sample timestamp_at_creation')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].controller_firmware_version,
                         'Sample controller_firmware_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].controller_serial, 'Sample controller_serial')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].save_displayed_chan_only,
                         'Sample save_displayed_chan_only')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_firmware_version,
                         'Sample headstage_firmware_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].qt_version, 'Sample qt_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].compile_date, 'Sample compile_date')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].compile_time, 'Sample compile_time')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].file_prefix, 'Sample file_prefix')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_gyro_sensor_on,
                         'Sample headstage_gyro_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_mag_sensor_on,
                         'Sample headstage_mag_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].trodes_version, 'Sample trodes_version')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].headstage_accel_sensor_on,
                         'Sample headstage_accel_sensor_on')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].commit_head, 'Sample commit_head')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].system_time_at_creation,
                         'Sample system_time_at_creation')
        self.assertEqual(self.nwb_content.devices['HeaderDevice1'].file_path, 'Sample file_path')
