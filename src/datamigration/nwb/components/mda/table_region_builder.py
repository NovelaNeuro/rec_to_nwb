
class TableRegionBuilder:

    def __init__(self, nwb_content, metadata):
        self.nwb_content = nwb_content
        self.metadata = metadata

    def build(self):
        return self.nwb_content.create_electrode_table_region(
            description=self.metadata['electrode region']['description'],
            region=self.metadata['electrode region']['region'],
            name='electrodes'
        )
