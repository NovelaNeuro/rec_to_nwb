from pynwb import ecephys

from src.datamigration.nwb_builder.binary_data import MdaData, MdaTimestamps
from src.datamigration.nwb_builder.data_iterator import DataIterator, DataIterator1D


class MdaExtractor:

    def __init__(self, mda_data, timestamps):
        self.mda_data = mda_data
        self.timestamps = timestamps
        print(timestamps)

    def get_mda(self, electrode_table_region):
        data = MdaData(self.mda_data)
        extracted_data = DataIterator(data, transpose=True)
        timestamps = MdaTimestamps([self.timestamps])
        extracted_timestamps = DataIterator1D(timestamps)
        series = ecephys.ElectricalSeries(name="e-series",
                                          data=extracted_data,
                                          electrodes=electrode_table_region,
                                          timestamps=extracted_timestamps,
                                          resolution=0.001,
                                          comments="sample comment",
                                          description="Electrical series registered on electrode")
        return series
