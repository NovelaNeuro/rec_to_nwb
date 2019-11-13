import os

import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import ecephys


class MdaExtractor:

    def __init__(self, path, timestamp_file_name, electrode_table_region):
        self.path = path
        self.timestamp_file_name = timestamp_file_name
        self.electrode_table_region = electrode_table_region

    def get_mda(self, file_number, data_chunk_size):
        if (file_number + data_chunk_size) > 64:  # add something from scanner
            data_chunk_size = 64 - file_number

        timestamps = readmda(self.path + self.timestamp_file_name)

        mda_files = [mda_file for mda_file in os.listdir(self.path) if
                     (mda_file.endswith('.mda') and mda_file != self.timestamp_file_name)]

        counter = 0
        series = []
        for j in range(data_chunk_size):
            file = mda_files[file_number + j]
            potentials = readmda(self.path + '/' + file)
            potentials_array = np.asarray(potentials)
            for i in range(4):
                series.append(ecephys.ElectricalSeries(name="e-series " + str((file_number + j) * 4 + i),
                                                       data=potentials_array[i],
                                                       electrodes=self.electrode_table_region,
                                                       timestamps=timestamps,
                                                       resolution=0.001,
                                                       comments="sample comment",
                                                       description="Electrical series registered on electrode "))
        return series
