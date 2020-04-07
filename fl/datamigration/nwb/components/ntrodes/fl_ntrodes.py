class FlNTrodes:

    def __init__(self, metadata, device, bad_channel, map_list):
        """internal representation of ntrodes data"""

        self.metadata = metadata
        self.device = device
        self.map_list = map_list
        self.bad_channel = bad_channel
