
class TableRegionBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

    def build(self, nwb_content):
        return nwb_content.create_electrode_table_region(
            description=self.metadata['electrode region']['description'],
            region=self.metadata['electrode region']['region'],
            name='electrodes'
        )