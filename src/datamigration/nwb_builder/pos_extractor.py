from pynwb.behavior import Position

from src.datamigration.nwb_builder.binary_data import PosData, PosTimestamps
from src.datamigration.nwb_builder.data_iterator import DataIterator, DataIterator1D


class POSExtractor:
    def __init__(self, datasets):
        self.datasets = datasets
        self.all_pos = []
        for dataset in datasets:
            data_from_current_dataset = [dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                                         dataset.get_all_data_from_dataset('pos') if
                                         (pos_file.endswith('.pos_online.dat'))]
            self.all_pos.append(data_from_current_dataset)
        print(self.all_pos)

    def get_position(self):
        pos_data = PosData(directories=self.all_pos)
        pos_timestamps = PosTimestamps(directories=self.all_pos)
        extracted_pos = DataIterator(pos_data)
        extracted_timestamps = DataIterator1D(pos_timestamps)
        position = Position()
        position.create_spatial_series(
            name=" The name of this TimeSeries dataset",
            data=extracted_pos,
            reference_frame="Description defining what the zero-position is",
            timestamps=extracted_timestamps
        )
        return position

