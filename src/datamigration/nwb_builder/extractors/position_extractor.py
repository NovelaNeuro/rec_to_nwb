from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb_builder.nwb_builder_tools.binary_data import PosData, PosTimestamps
from src.datamigration.nwb_builder.nwb_builder_tools.data_iterator import DataIterator, DataIterator1D


# TODO Is it SOLID?
class PositionExtractor:
    def __init__(self, datasets):
        self.datasets = datasets
        self.all_pos = []
        self.continuous_time = []

        for dataset in datasets:
            data_from_current_dataset = [dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                                         dataset.get_all_data_from_dataset('pos') if
                                         (pos_file.endswith('.pos_online.dat'))]
            if data_from_current_dataset is None or dataset.get_continuous_time() is None:
                raise MissingDataException("Incomplete data in dataset "
                                           + str(dataset.name)
                                           + "missing continuous time file")
            self.all_pos.append(data_from_current_dataset)
            self.continuous_time.append(dataset.get_continuous_time())

    def get_position(self):
        pos_data = PosData(directories=self.all_pos)
        extracted_pos = DataIterator(pos_data)
        return extracted_pos

    def get_timestamps(self):
        pos_timestamps = PosTimestamps(directories=self.all_pos, continuous_time_directories=self.continuous_time)
        extracted_timestamps = DataIterator1D(pos_timestamps)

        return extracted_timestamps


