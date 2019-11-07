import os

from mountainlab_pytools.mdaio import readmda


class MdaExtractor:

    def __init__(self, path, timestamp_file_name):
        self.path = path
        self.timestamp_file_name = timestamp_file_name

    def get_mda(self):
        timestamps = readmda(self.path + '/' + self.timestamp_file_name)

        mda_files = [mda_file for mda_file in os.listdir(self.path) if
                     (mda_file.endswith('.mda') and mda_file != self.timestamp_file_name)]

        counter = 0
        for file in mda_files:
            electrode_table_region = nwbfile.create_electrode_table_region([counter % 4], "sample description")
            name = "e-series" + str(counter)
            series = ecephys.ElectricalSeries(name,
                                              readmda(self.path + '/' + file)[counter % 4],
                                              electrode_table_region,
                                              timestamps=timestamps,
                                              # Alternatively, could specify starting_time and rate as follows
                                              # starting_time=ephys_timestamps[0],
                                              # rate=rate,
                                              resolution=0.001,
                                              comments="sample comment",
                                              description="Electrical series registered on electrode " + str(counter))
            nwbfile.add_acquisition(series)
            counter = counter + 1

