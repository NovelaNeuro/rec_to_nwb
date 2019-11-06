from mountainlab_pytools.mdaio import readmda

from src.e2etests.integration.experiment_data import ExperimentData


class MdaExtractor:

    def __init__(self,
                 path_to_mda='../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.mda'):
        self.path_to_mda = path_to_mda

    def get_mda(self):
        timestamps = readmda(ExperimentData.mda_path + ExperimentData.mda_timestamp)

        mda_files = [mda_file for mda_file in os.listdir(ExperimentData.mda_path) if
                     (mda_file.endswith('.mda') and mda_file != ExperimentData.mda_timestamp)]

        counter = 0
        for file in mda_files:
            electrode_table_region = nwbfile.create_electrode_table_region([counter % 4], "description")
            name = "test" + str(counter)
            series = ecephys.ElectricalSeries(name,
                                              readmda(ExperimentData.mda_path + ExperimentData.mda_file)[counter % 4],
                                              electrode_table_region,
                                              timestamps=timestamps,
                                              # Alternatively, could specify starting_time and rate as follows
                                              # starting_time=ephys_timestamps[0],
                                              # rate=rate,
                                              resolution=0.001,
                                              comments="aaa",
                                              description="Electrical series registered on electrode " + str(counter))
            nwbfile.add_acquisition(series)
            counter = counter + 1
