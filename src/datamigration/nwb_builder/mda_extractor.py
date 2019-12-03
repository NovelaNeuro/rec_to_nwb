import os

import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import ecephys

from src.datamigration.nwb_builder.data_iterator import DataIterator


class MdaExtractor:

    def __init__(self, path, mda_data, timestamps):
        self.mda_data_paths = mda_data_paths[0]
        self.timestamps = timestamps

    def get_mda(self, electrode_table_region):
        for path in self.mda_data:
            mda_names = [mda_file for mda_file in os.listdir(self.mda_data_paths) if
                         (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]
            mda_files = []
            for mda_file in mda_names:
                mda_files.append(path + mda_file)
        array_from_single_mda = readmda(mda_files[0])
        mda_len = np.size(array_from_single_mda, 1)
        mda_num_rows = np.size(array_from_single_mda, 0)
        del array_from_single_mda
        data = DataIterator(mda_files, mda_len, mda_num_rows, len(self.mda_data_paths))

        series = ecephys.ElectricalSeries(name="e-series",
                                          data=data,
                                          electrodes=electrode_table_region,
                                          timestamps=self.timestamps,
                                          resolution=0.001,
                                          comments="sample comment",
                                          description="Electrical series registered on electrode")
        return series
