from .device import Device


class HardwareConfiguration:

    def __init__(self, element):
        self.tree = element
        self.devices = [Device(device_element) for device_element in self.tree.findall('Device')]
        self.tag = self.tree.tag
        self.sampling_rate = self.tree.get('samplingRate')
        self.num_channels = self.tree.get('numChannels')