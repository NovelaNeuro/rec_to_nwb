from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device import FlCameraDevice
from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device_manager import FlCameraDeviceManager


class TestFlCameraDeviceManager(TestCase):

    def test_fl_camera_device_manager_created_successfully(self):
        metadata = {
            'cameras': [
                {'id': 0, 'meters_per_pixel': 0.02},
                {'id': 1, 'meters_per_pixel': 3},
                {'id': 2, 'meters_per_pixel': '0.05'},
            ]
        }

        fl_camera_device_manager = FlCameraDeviceManager(metadata)
        fl_camera_devices = fl_camera_device_manager.get_fl_device_manager()

        self.assertIsInstance(fl_camera_devices, list)
        self.assertIsInstance(fl_camera_devices[0], FlCameraDevice)

        self.assertEqual(fl_camera_devices[0].name, 'camera_device 0')
        self.assertEqual(fl_camera_devices[0].meters_per_pixel, 0.02)
        self.assertEqual(fl_camera_devices[1].name, 'camera_device 1')
        self.assertEqual(fl_camera_devices[1].meters_per_pixel, 3.0)
        self.assertEqual(fl_camera_devices[2].name, 'camera_device 2')
        self.assertEqual(fl_camera_devices[2].meters_per_pixel, 0.05)

    @should_raise(NoneParamException)
    def test_fl_camera_device_manager_failed_due_to_none_key_in_metadata(self):
        metadata = {
            'cameras': [
                {'id': 0, 'meters_per_pixel': 0.02},
                {'id': 1, 'meters_per_pixel': 3},
                {'id': 2},
            ]
        }

        fl_camera_device_manager = FlCameraDeviceManager(metadata)
        fl_camera_device_manager.get_fl_device_manager()

    @should_raise(TypeError)
    def test_fl_camera_device_manager_failed_init_due_to_none_param(self):
        FlCameraDeviceManager(None)
