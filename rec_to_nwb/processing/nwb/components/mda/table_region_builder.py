
class TableRegionBuilder:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content

    def build(self):
        return self.nwb_content.create_electrode_table_region(
            description='-',
            region=list(range(len(self.nwb_content.electrodes))),
            name='electrodes'
        )
