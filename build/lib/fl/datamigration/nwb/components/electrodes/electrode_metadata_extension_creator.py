class ElectrodesMetadataExtensionCreator:
    def __init__(self):
        self.rel_x = []
        self.rel_y = []
        self.rel_z = []

    def create_extensions(self, electrode):
        self.rel_x.append(electrode['rel_x'])
        self.rel_y.append(electrode['rel_y'])
        self.rel_z.append(electrode['rel_z'])
