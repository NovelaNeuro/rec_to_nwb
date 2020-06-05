import logging.config
import os

from rec_to_nwb.processing.nwb.components.device.device_factory import DeviceFactory
from rec_to_nwb.processing.nwb.components.device.device_injector import DeviceInjector
from rec_to_nwb.processing.nwb.components.device.header.fl_header_device_manager import FlHeaderDeviceManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HeaderDeviceOriginator:

    def __init__(self, header):
        self.fl_header_device_manager = FlHeaderDeviceManager(
            'header_device',
            header.configuration.global_configuration
        )
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

    def make(self, nwb_content):
        logger.info('HeaderDevice: Building')
        fl_header_device = self.fl_header_device_manager.get_fl_header_device()
        logger.info('HeaderDevice: Creating')
        header_device = self.device_factory.create_header_device(fl_header_device)
        logger.info('HeaderDevice: Injecting into NWB')
        self.device_injector.inject_all_devices(nwb_content, [header_device])
