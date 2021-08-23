import logging.config
import os

from rec_to_nwb.processing.nwb.components.device.acq.fl_data_acq_device_manager import \
    FlDataAcqDeviceManager

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DataAcqDeviceOriginator:
    def __init__(self, device_factory, device_injector, metadata):
        self.device_factory = device_factory
        self.device_injector = device_injector

        self.fl_data_acq_device_manager = FlDataAcqDeviceManager(metadata)

    def make(self, nwb_content):
        logger.info('FlDataAcqDevice: Building')
        fl_data_acq_devices = self.fl_data_acq_device_manager.get_fl_data_acq_device()
        logger.info('FlDataAcqDevice: Creating DataAcqDevice')
        data_acq_device = [self.device_factory.create_data_acq_device(fl_data_acq_device)
                           for fl_data_acq_device in fl_data_acq_devices]
        logger.info('FlDataAcqDevice: Injecting DataAcqDevice into NWB')
        self.device_injector.inject_all_devices(nwb_content, data_acq_device)
