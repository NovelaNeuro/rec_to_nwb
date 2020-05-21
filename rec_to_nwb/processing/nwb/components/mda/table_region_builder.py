
class TableRegionBuilder:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content

    def build(self):
        return self.nwb_content.create_electrode_table_region(
            description='-',
            region=self.__get_region(),
            name='electrodes'
        )

    def __get_region(self):
        return list(range(len(self.nwb_content.electrodes)))
