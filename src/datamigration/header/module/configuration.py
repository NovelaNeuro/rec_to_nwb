import logging.config
import os

from src.datamigration.header.module.aux_display_configuration import AuxDisplayConfiguration
from src.datamigration.header.module.global_configuration import GlobalConfiguration
from src.datamigration.header.module.hardware_configuration import HardwareConfiguration
from src.datamigration.header.module.module_configuration import ModuleConfiguration
from src.datamigration.header.module.spike_configuration import SpikeConfiguration
from src.datamigration.header.module.stream_display import StreamDisplay

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Configuration:

    def __init__(self, element):
        self.tree = element
        self.module_configuration = ModuleConfiguration(self.tree.find('ModuleConfiguration'))
        self.global_configuration = GlobalConfiguration(self.tree.find('GlobalConfiguration'))
        self.spike_configuration = SpikeConfiguration(self.tree.find('SpikeConfiguration'))
        self.stream_display = StreamDisplay(self.tree.find('StreamDisplay'))
        self.hardware_configuration = HardwareConfiguration(self.tree.find('HardwareConfiguration'))
        self.aux_display_configuration = AuxDisplayConfiguration(self.tree.find('AuxDisplayConfiguration'))
        self.tag = self.tree.tag
