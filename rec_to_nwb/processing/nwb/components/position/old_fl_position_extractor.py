from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_timestamp_iterator import MultiThreadTimestampIterator
from rec_to_nwb.processing.nwb.components.position.old_pos_timestamp_manager import OldPosTimestampManager
from rec_to_nwb.processing.nwb.components.position.pos_data_manager import PosDataManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class OldFlPositionExtractor:

    @beartype
    def __init__(self, datasets: list):
        self.datasets = datasets
        self.all_pos = self.__extract_data()

    def __extract_data(self):
        all_pos = []
        for dataset in self.datasets:
            data_from_current_dataset = [
                dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                dataset.get_all_data_from_dataset('pos') if
                (pos_file.endswith('.pos_online.dat'))]
            all_pos.append(data_from_current_dataset)
        return all_pos

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
        old_pos_timestamp_managers = [
            OldPosTimestampManager(
                directories=[single_pos],
            )
            for single_pos in self.all_pos
        ]
        return [
            MultiThreadTimestampIterator(old_pos_timestamp_manager)
            for old_pos_timestamp_manager in old_pos_timestamp_managers
        ]
