
class TableRegionBuilder:

    def __init__(self, nwb_content, metadata):
        self.metadata = metadata
        self.nwb_content = nwb_content

    def build(self):
        return self.nwb_content.create_electrode_table_region(
            description=self.metadata['electrode region']['description'],
            region=self.metadata['electrode region']['region'],
            name='electrodes'
        )
