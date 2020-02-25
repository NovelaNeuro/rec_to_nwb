from src.datamigration.nwb.components.mda.mda_builder import MdaBuilder
from src.datamigration.nwb.components.mda.table_region_builder import TableRegionBuilder
from src.datamigration.nwb.components.mda.mda_extractor import MdaExtractor


class MdaManager:
    def __init__(self, nwb_content, metadata, sampling_rate, datasets):
        self.__table_region_builder = TableRegionBuilder(nwb_content, metadata)
        self.__mda_extractor = MdaExtractor(datasets)
        self.__mda_builder = MdaBuilder(sampling_rate)

    def get_data(self):
        electrode_table_region = self.__table_region_builder.build()
        data = self.__mda_extractor.get_data()
        return self.__mda_builder.build(electrode_table_region, data)
