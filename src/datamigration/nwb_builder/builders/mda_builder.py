from src.datamigration.nwb_builder.creators.mda_creator import MdaCreator
from src.datamigration.nwb_builder.managers.mda_manager import MdaManager


class MDABuilder:

    def __init__(self, metadata, header, datasets):
        self.mda_manager = MdaManager(metadata, header, datasets)
        self.mda_creator = MdaCreator()

    def build(self):
        sampling_rate = self.mda_manager.get_sampling_rate()
        electrode_table_region = self.mda_manager.get_electrode_table_region()
        extracted_mda_data = self.mda_manager.get_extracted_mda_data()

        mda = self.mda_creator.create_mda(sampling_rate, electrode_table_region, extracted_mda_data)



