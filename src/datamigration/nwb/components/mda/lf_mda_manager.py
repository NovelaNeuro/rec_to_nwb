from src.datamigration.nwb.components.mda.lf_mda_builder import LfMdaBuilder
from src.datamigration.nwb.components.mda.table_region_builder import TableRegionBuilder
from src.datamigration.nwb.components.mda.lf_mda_extractor import LfMdaExtractor


class LfMdaManager:
    def __init__(self, nwb_content, metadata, sampling_rate, datasets):
        self.__table_region_builder = TableRegionBuilder(nwb_content, metadata)
        self.__lf_mda_extractor = LfMdaExtractor(datasets)
        self.__lf_mda_builder = LfMdaBuilder(sampling_rate)

    def get_data(self):
        electrode_table_region = self.__table_region_builder.build()
        data = self.__lf_mda_extractor.get_data()
        return self.__lf_mda_builder.build(electrode_table_region, data)
