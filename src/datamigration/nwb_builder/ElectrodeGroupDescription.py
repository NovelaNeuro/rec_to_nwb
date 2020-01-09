class ElectrodeGroupDescription:
    def __init__(self, eg_dict):
        self.id = eg_dict['id']
        self.location = eg_dict['location']
        self.device = eg_dict['device']
        self.probe_id = eg_dict['probe_id']
