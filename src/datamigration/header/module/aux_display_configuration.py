import logging.config
import os

from src.datamigration.header.module.disp_channel import DispChannel

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class AuxDisplayConfiguration:

    def __init__(self, element):
        self.tree = element
        self.disp_channels = [DispChannel(disp_channel_element) for disp_channel_element
                              in self.tree.findall('DispChannel')]
        self.tag = self.tree.tag