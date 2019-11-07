import os

import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import ecephys


class MdaExtractor:

    def __init__(self, path, timestamp_file_name, electrode_table_region):
        self.path = path
        self.timestamp_file_name = timestamp_file_name
        self.electrode_table_region = electrode_table_region


    def get_mda(self):
        timestamps = readmda(self.path + '/' + self.timestamp_file_name)

        mda_files = [mda_file for mda_file in os.listdir(self.path) if
                     (mda_file.endswith('.mda') and mda_file != self.timestamp_file_name)]

        counter = 0
        series = []
        for file in mda_files:
            potentials = readmda(self.path + '/' + file),
            potentials_array = np.asarray(potentials)
            for i in range(4):
                name = "e-series " + str(counter)
                series.append(ecephys.ElectricalSeries(name,
                                                       potentials_array[0, i],
                                                       self.electrode_table_region,
                                                       timestamps=timestamps,
                                                       # Alternatively, could specify starting_time and rate as follows
                                                       # starting_time=ephys_timestamps[0],
                                                       # rate=rate,
                                                       resolution=0.001,  # todo should we set up this in matadata.yml?
                                                       comments="sample comment",
                                                       description="Electrical series registered on electrode " + str(
                                                           counter)))
                counter = counter + 1
        return series
