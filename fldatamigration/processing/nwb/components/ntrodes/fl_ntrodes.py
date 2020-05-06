class FlNTrodes:

    def __init__(self, metadata, device, bad_channels, map_list):
        """internal representation of ntrodes data"""

        self.metadata = metadata
        self.device = device
        self.map_list = map_list
        self.bad_channels = bad_channels
