from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_timestamp_iterator import MultiThreadTimestampIterator
from rec_to_nwb.processing.nwb.components.position.pos_data_manager import PosDataManager
from rec_to_nwb.processing.nwb.components.position.pos_timestamp_manager import PosTimestampManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPositionExtractor:

    @beartype
    def __init__(self, datasets: list, convert_timestamps: bool = True):
        self.datasets = datasets
        self.all_pos, self.continuous_time = self.__extract_data()
        self.convert_timestamps = convert_timestamps

    def __extract_data(self):
        all_pos = []
        continuous_time = []
        for dataset in self.datasets:
            data_from_current_dataset = [
                dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                dataset.get_all_data_from_dataset('pos') if
                (pos_file.endswith('.pos_online.dat'))]
            if dataset.get_continuous_time() is None:
                raise MissingDataException(
                    'Incomplete data in dataset '
                    + str(dataset.name)
                    + 'missing continuous time file')
            all_pos.append(data_from_current_dataset)
            continuous_time.append(dataset.get_continuous_time())
        return all_pos, continuous_time

    def get_positions(self):
        pos_datas = [
            PosDataManager(directories=[single_pos])
            for single_pos in self.all_pos
        ]
        return [
            MultiThreadDataIterator(pos_data)
            for pos_data in pos_datas
        ]

    def get_columns_labels(self):
        pos_datas = [
            PosDataManager(directories=[single_pos])
            for single_pos in self.all_pos
        ]
        return [
            pos_data.get_column_labels_as_string()
            for pos_data in pos_datas
        ]

    def get_timestamps(self):
        pos_timestamp_managers = [
            PosTimestampManager(
                directories=[single_pos],
                continuous_time_directories=[continuous_time],
                convert_timestamps = self.convert_timestamps
            )
            for single_pos, continuous_time in zip(self.all_pos, self.continuous_time)
        ]
        return [
            MultiThreadTimestampIterator(pos_timestamp_manager)
            for pos_timestamp_manager in pos_timestamp_managers
        ]
