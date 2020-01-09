class NTrode:
    def __init__(self, ntrode_dict):
        self.id = ntrode_dict['ntrode_id']
        self.probe_id = ntrode_dict['probe_id']
        self.channel_map = ntrode_dict['map']
