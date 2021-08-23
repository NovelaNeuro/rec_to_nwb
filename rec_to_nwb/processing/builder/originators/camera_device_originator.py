import logging.config
import os

from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device_manager import \
    FlCameraDeviceManager
from rec_to_nwb.processing.nwb.components.device.device_factory import \
    DeviceFactory
from rec_to_nwb.processing.nwb.components.device.device_injector import \
    DeviceInjector

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class CameraDeviceOriginator:

    def __init__(self, metadata):
        self.fl_camera_device_manager = FlCameraDeviceManager(metadata)
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

    def make(self, nwb_content):
        logger.info('CameraDevice: Building')
        fl_camera_devices = self.fl_camera_device_manager.get_fl_device_manager()
        logger.info('CameraDevice: Creating')
        camera_devices = [self.device_factory.create_camera_device(single_camera_device)
                          for single_camera_device in fl_camera_devices]
        logger.info('CameraDevice: Injecting into NWB')
        self.device_injector.inject_all_devices(nwb_content, camera_devices)
