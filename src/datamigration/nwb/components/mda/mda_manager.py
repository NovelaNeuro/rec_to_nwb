from src.datamigration.nwb.components.mda.mda_extractor import MdaExtractor
from src.datamigration.nwb.components.table_region.table_region_builder import TableRegionBuilder


class MdaManager:
    def __init__(self, metadata, header, datasets):
        self.header = header
        self.table_region_builder = TableRegionBuilder(metadata)
        self.mda_extractor = MdaExtractor(datasets)

    def get_sampling_rate(self):
        return self.header.configuration.hardware_configuration.sampling_rate

    def get_electrode_table_region(self, nwb_content):#todo why we touch nwb_content in here?
        return self.table_region_builder.build(nwb_content)

    def get_data(self):
        return self.mda_extractor.get_data()
