import xml.etree.ElementTree as ET


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.configuration = Configuration(self.tree)

    def configuration(self):
        return self.tree.getroot()


class Configuration:

    def __init__(self, tree):
        self.tree = tree
        self.module_configuration = ModuleConfiguration(self.tree)
        self.global_configuration = GlobalConfiguration(self.tree)
        self.spike_configuration = SpikeConfiguration(self.tree)
        self.stream_display = StreamDisplay(self.tree)
        self.hardware_configuration = HardwareConfiguration(self.tree)
        self.aux_display_configuration = AuxDisplayConfiguration(self.tree)

    def module_configuration(self):
        return self.tree.getroot().find('ModuleConfiguration')

    def global_configuration(self):
        return self.tree.getroot().find('GlobalConfiguration')

    def spike_configuration(self):
        return self.tree.getroot().find('SpikeConfiguration')

    def stream_configuration(self):
        return self.tree.getroot().find('StreamConfiguration')

    def hardware_configuration(self):
        return self.tree.getroot().find('HardwareConfiguration')

    def aux_display_configuration(self):
        return self.tree.getroot().find('AuxDisplayConfiguration')


class ModuleConfiguration:

    def __init__(self, tree):
        self.tree = tree
        self.single_module_configurations = [SingleModuleConfiguration(self.tree), SingleModuleConfiguration(self.tree)]

    def single_module_configurations(self):
        return self.tree.getroot().find('ModuleConfiguration').findall('SingleModuleConfiguration')


class SingleModuleConfiguration:

    def __init__(self, tree):
        self.tree = tree
        self.napis = 'napis'


class GlobalConfiguration:

    def __init__(self, tree):
        self.tree = tree


class SpikeConfiguration:

    def __init__(self, tree):
        self.tree = tree


class AuxDisplayConfiguration:

    def __init__(self, tree):
        self.tree = tree


class StreamDisplay:

    def __init__(self, tree):
        self.tree = tree


class HardwareConfiguration:

    def __init__(self, tree):
        self.tree = tree






