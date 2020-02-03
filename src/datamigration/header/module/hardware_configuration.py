import logging.config
import os

from src.datamigration.header.module.device import Device

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class HardwareConfiguration:

    def __init__(self, element):
        self.tree = element
        self.devices = [Device(device_element) for device_element in self.tree.findall('Device')]
        self.tag = self.tree.tag
        self.sampling_rate = self.tree.get('samplingRate')
        self.num_channels = self.tree.get('numChannels')