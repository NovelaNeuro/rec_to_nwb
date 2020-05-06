class FlNwbElectrodeGroup:

    def __init__(self, name, description, location, device, targeted_location,
                 targeted_x, targeted_y, targeted_z, units):
        self.name = name
        self.description = description
        self.location = location
        self.device = device
        self.targeted_location = targeted_location
        self.targeted_x = targeted_x
        self.targeted_y = targeted_y
        self.targeted_z = targeted_z
        self.units = units
