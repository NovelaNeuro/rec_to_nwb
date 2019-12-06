from pynwb import ecephys

from src.datamigration.nwb_builder.binary_data import MdaData


class MdaExtractor:

    def __init__(self, mda_data, timestamps):
        self.mda_data = mda_data
        self.timestamps = timestamps

    def get_mda(self, electrode_table_region):
        data = MdaData(self.mda_data)
        series = ecephys.ElectricalSeries(name="e-series",
                                          data=data,
                                          electrodes=electrode_table_region,
                                          timestamps=self.timestamps,
                                          resolution=0.001,
                                          comments="sample comment",
                                          description="Electrical series registered on electrode")
        return series
