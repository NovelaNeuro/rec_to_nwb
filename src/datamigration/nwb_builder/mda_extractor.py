from pynwb import ecephys

from src.datamigration.nwb_builder.binary_data import MdaData, MdaTimestamps
from src.datamigration.nwb_builder.data_iterator import DataIterator, DataIterator1D


class MdaExtractor:

    def __init__(self, datasets):
        self.mda_data = []
        self.timestamps = []
        self.continuous_time = []
        for dataset in datasets:
            data_from_current_dataset = [dataset.get_data_path_from_dataset('mda') + mda_file for mda_file in
                                         dataset.get_all_data_from_dataset('mda') if
                                         (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]
            self.mda_data.append(data_from_current_dataset)
            self.timestamps.append(dataset.get_mda_timestamps())
            self.continuous_time.append(dataset.get_continuous_time())

    def get_mda(self, electrode_table_region, sampling_rate):
        data = MdaData(self.mda_data)
        extracted_data = DataIterator(data)
        timestamps = MdaTimestamps([self.timestamps], [self.continuous_time])
        extracted_timestamps = DataIterator1D(timestamps)
        series = ecephys.ElectricalSeries(name="e-series",
                                          data=extracted_data,
                                          electrodes=electrode_table_region,
                                          timestamps=extracted_timestamps,
                                          resolution=sampling_rate,
                                          comments="sample comment",
                                          description="Electrical series registered on electrode")
        return series
