import pandas as pd
from pynwb.behavior import Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class POSExtractor:

    # From this location this won`t work. We want to create more relative path in ExperimentData? (ExperimentData.pos_path + ExperimentData.pos_file)
    def __init__(self,
                 path_to_pos='../e2etests/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.1.pos/20190718_beans_01_s1.1.pos_online.dat'):
        self.path_to_pos = path_to_pos

    def get_position(self):
        self.pos_online = readTrodesExtractedDataFile(self.path_to_pos)
        position_online = pd.DataFrame(self.pos_online['data'])
        position = Position()
        position.create_spatial_series(
            name=" The name of this TimeSeries dataset",
            data=(position_online.xloc, position_online.yloc, position_online.xloc2, position_online.yloc2),
            reference_frame="Description defining what the zero-position is",
            timestamps=position_online.time.tolist()
        )
        return position
