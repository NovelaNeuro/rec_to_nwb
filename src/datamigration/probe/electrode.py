class Electrode:

    def __init__(self, electrode_dict):
        self.name = electrode_dict[0][0]
        self.rel_x = electrode_dict[0][1]['rel_x']
        self.rel_y = electrode_dict[0][1]['rel_y']
        self.rel_z = electrode_dict[0][1]['rel_z']