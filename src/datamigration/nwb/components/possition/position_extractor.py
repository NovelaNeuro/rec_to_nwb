from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb_builder.iterators.data_iterator_1_dim import DataIterator1D
from src.datamigration.nwb_builder.iterators.data_iterator_2_dim import DataIterator2D
from src.datamigration.nwb.components.possition.pos_data_manager import PosDataManager
from src.datamigration.nwb.components.possition.pos_timestamp_manager import PosTimestampManager


class PositionExtractor:
    def __init__(self, datasets):
        self.datasets = datasets
        self.all_pos, self.continuous_time = self.__extract_data()

    def __extract_data(self):
        all_pos = []
        continuous_time = []
        for dataset in self.datasets:
            data_from_current_dataset = [
                dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                dataset.get_all_data_from_dataset('pos') if
                (pos_file.endswith('.pos_online.dat'))]
            if data_from_current_dataset is None or dataset.get_continuous_time() is None:
                raise MissingDataException(
                    "Incomplete data in dataset "
                    + str(dataset.name)
                    + "missing continuous time file")
            all_pos.append(data_from_current_dataset)
            continuous_time.append(dataset.get_continuous_time())
        return all_pos, continuous_time

    def get_position(self):
        pos_data = PosDataManager(directories=self.all_pos)
        return DataIterator2D(pos_data)

    def get_timestamps(self):
        pos_timestamps = PosTimestampManager(
            directories=self.all_pos,
            continuous_time_directories=self.continuous_time)
        return DataIterator1D(pos_timestamps)
