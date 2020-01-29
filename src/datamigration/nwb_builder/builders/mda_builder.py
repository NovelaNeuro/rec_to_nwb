from pynwb import ecephys

from src.datamigration.nwb_builder.builders.table_region_builder import TableRegionBuilder
from src.datamigration.nwb_builder.extractors.mda_extractor import MdaExtractor


class MDABuilder:

    def __init__(self, metadata, header, datasets):
        self.header = header
        self.metadata = metadata
        self.datasets = datasets

    def build(self):
        sampling_rate = self.header.configuration.hardware_configuration.sampling_rate
        electrode_table_region = TableRegionBuilder(self.metadata).build()

        extracted_mda_data = MdaExtractor(self.datasets).get_mda_data()

        mda_series = ecephys.ElectricalSeries(name="e-series",
                                              data=extracted_mda_data.mda_data,
                                              electrodes=electrode_table_region,
                                              timestamps=extracted_mda_data.mda_timestamsp,
                                              resolution=sampling_rate,
                                              comments="sample comment",
                                              description="Electrical series registered on electrode")
        return mda_series

