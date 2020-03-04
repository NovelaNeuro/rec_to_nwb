from .aux_display_configuration import AuxDisplayConfiguration
from .global_configuration import GlobalConfiguration
from .hardware_configuration import HardwareConfiguration
from .module_configuration import ModuleConfiguration
from .spike_configuration import SpikeConfiguration
from .stream_display import StreamDisplay


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
