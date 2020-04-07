from .disp_channel import DispChannel


class AuxDisplayConfiguration:

    def __init__(self, element):
        self.tree = element
        self.disp_channels = [DispChannel(disp_channel_element) for disp_channel_element
                              in self.tree.findall('DispChannel')]
        self.tag = self.tree.tag