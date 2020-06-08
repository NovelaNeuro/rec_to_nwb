class FlProbe:

    def __init__(self, probe_id, name, probe_type, units, probe_description, contact_side_numbering,
                 contact_size, shanks):
        self.probe_id = probe_id
        self.name = name
        self.probe_type = probe_type
        self.units = units
        self.probe_description = probe_description
        self.contact_side_numbering = contact_side_numbering
        self.contact_size = contact_size
        self.shanks = shanks
