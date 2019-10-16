import xml.etree.ElementTree as ET


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.configuration = Configuration(self.tree.getroot())

    def get_configuration(self):
        return Configuration(self.tree.getroot())


class Configuration:

    def __init__(self, element):
        self.tree = element
        self.module_configuration = ModuleConfiguration(self.tree)
        self.global_configuration = GlobalConfiguration(self.tree)
        self.spike_configuration = SpikeConfiguration(self.tree)
        self.stream_display = StreamDisplay(self.tree)
        self.hardware_configuration = HardwareConfiguration(self.tree)
        self.aux_display_configuration = AuxDisplayConfiguration(self.tree)

    def get_module_configuration(self):
        return ModuleConfiguration(self.tree.find('ModuleConfiguration'))

    def get_hardware_configuration(self):
        return HardwareConfiguration(self.tree.find('HardwareConfiguration'))

    def get_global_configuration(self):
        return GlobalConfiguration(self.tree.find('GlobalConfiguration'))

    def get_spike_configuration(self):
        return SpikeConfiguration(self.tree.find('SpikeConfiguration'))

    def get_aux_display_configuration(self):
        return AuxDisplayConfiguration(self.tree.find('AuxDisplayConfiguration'))

    def get_stream_display(self):
        return StreamDisplay(self.tree.find('StreamDisplay'))


class ModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.single_module_configuration_elements = list(self.tree)
        self.single_module_configurations = \
            [SingleModuleConfiguration(single_module_configuration_element)
             for single_module_configuration_element in self.single_module_configuration_elements]

    def get_single_module_configurations(self):
        return self.single_module_configurations


class SingleModuleConfiguration:

    def __init__(self, element):
        self.tree = element
        self.argument_elements = list(self.tree)
        self.arguments = \
            [Argument(argument_element) for argument_element in self.argument_elements]

    def get_arguments(self):
        return self.arguments


class Argument:

    def __init__(self, element):
        self.tree = element


class GlobalConfiguration:

    def __init__(self, element):
        self.tree = element


class HardwareConfiguration:

    def __init__(self, element):
        self.tree = element
        self.device_elements = list(self.tree)
        self.devices = [Device(device_element) for device_element in self.device_elements]

    def get_devices(self):
        return self.devices


class Device:

    def __init__(self, element):
        self.tree = element
        self.channel_elements = list(self.tree)
        self.channels = \
            [Channel(channel_element) for channel_element in self.channel_elements]

    def get_channels(self):
        return self.channels


class Channel:

    def __init__(self, element):
        self.tree = element


class StreamDisplay:

    def __init__(self, element):
        self.tree = element


class AuxDisplayConfiguration:

    def __init__(self, element):
        self.tree = element
        self.disp_channel_elements = list(self.tree)
        self.disp_channels = [DispChannel(disp_channel_element) for disp_channel_element in self.disp_channel_elements]

    def get_disp_channels(self):
        return self.disp_channels


class DispChannel:

    def __init__(self, element):
        self.tree = element


class SpikeConfiguration:

    def __init__(self, element):
        self.tree = element
        self.spike_n_trode_elements = list(self.tree)
        self.spike_n_trodes = [SpikeNTrode(spike_n_trode_element) for spike_n_trode_element in self.spike_n_trode_elements]

    def get_spike_n_trodes(self):
        return self.spike_n_trodes


class SpikeNTrode:

    def __init__(self, element):
        self.tree = element
        self.spike_channel_elements = list(self.tree)
        self.spike_channels = [SpikeChannel(spike_channel_element) for spike_channel_element in self.spike_channel_elements]

    def get_spike_channels(self):
        return self.spike_channels


class SpikeChannel:

    def __init__(self, element):
        self.tree = element
