from .channel import Channel


class Device:

    def __init__(self, element):
        self.tree = element
        self.channels = \
            [Channel(channel_element) for channel_element in self.tree.findall('Channel')]
        self.tag = self.tree.tag
        self.name = self.tree.get('name')
        self.num_bytes = self.tree.get('numBytes')
        self.available = self.tree.get('available')
        self.packet_order_preference = self.tree.get('packetOrderPreference')