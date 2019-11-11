import pandas as pd
from pynwb.behavior import Position
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class POSExtractor:
    def __init__(self, path):
        self.path = path
        self.pos_online = None

    def get_position(self):
        self.pos_online = readTrodesExtractedDataFile(self.path)
        df_position = pd.DataFrame(self.pos_online['data'])
        position = Position()
        position.create_spatial_series(
            name=" The name of this TimeSeries dataset",
            data=(df_position.xloc, df_position.yloc, df_position.xloc2, df_position.yloc2),
            reference_frame="Description defining what the zero-position is",
            timestamps=df_position.time.tolist()
        )
        return position

