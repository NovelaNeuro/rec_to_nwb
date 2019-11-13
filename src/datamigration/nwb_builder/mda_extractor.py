import os

import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import ecephys


class MdaExtractor:

    def __init__(self, path, timestamps):
        self.path = path
        self.timestamps = timestamps

    def get_mda(self, first_file_number, data_chunk_size, electrode_table_region):
        if (first_file_number + data_chunk_size) > 64:  # add something from scanner
            data_chunk_size = 64 - first_file_number

        mda_files = [mda_file for mda_file in os.listdir(self.path) if
                     (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]
        counter = 0
        series = []
        for file_number in range(data_chunk_size):
            current_file_number = first_file_number + file_number
            file = mda_files[current_file_number]
            potentials = readmda(self.path + '/' + file)
            potentials_array = np.asarray(potentials)
            for series_number in range(4):
                series.append(ecephys.ElectricalSeries(name="e-series " + str(current_file_number * 4 + series_number),
                                                       data=potentials_array[series_number],
                                                       electrodes=electrode_table_region,
                                                       timestamps=self.timestamps,
                                                       resolution=0.001,
                                                       comments="sample comment",
                                                       description="Electrical series registered on electrode "))
        return series
