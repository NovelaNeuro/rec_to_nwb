from hdmf.common import DynamicTableRegion


class TableRegionBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

    def build(self):
        region = DynamicTableRegion(
            description=self.metadata['electrode region']['description'],
            region=self.metadata['electrode region']['region'],
            name='electrodes'
        )
        return region
