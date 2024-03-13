"""Gets the online position tracking directories and retrieve position and
timestamps"""
import os

from rec_to_nwb.processing.exceptions.missing_data_exception import \
    MissingDataException
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import \
    MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_timestamp_iterator import \
    MultiThreadTimestampIterator
from rec_to_nwb.processing.nwb.components.position.pos_data_manager import \
    PosDataManager
from rec_to_nwb.processing.nwb.components.position.pos_timestamp_manager import \
    PosTimestampManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlPositionExtractor:

    @beartype
    def __init__(self, datasets: list, convert_timestamps: bool = True):
        self.datasets = datasets
        (self.all_position_directories,
         self.continuous_time_directories) = self.__extract_data()
        self.convert_timestamps = convert_timestamps

    def __extract_data(self):
        """Gets online position tracking file and corresponding continuous
        time file"""
        all_position_directories = []
        continuous_time_directories = []
        for dataset in self.datasets:
            pos_online_paths = [
                os.path.join(
                    dataset.get_data_path_from_dataset('pos'), pos_file)
                for pos_file in dataset.get_all_data_from_dataset('pos')
                if pos_file.endswith('.pos_online.dat')]

            if dataset.get_continuous_time() is None:
                raise MissingDataException(
                    'Incomplete data in dataset '
                    + str(dataset.name)
                    + 'missing continuous time file')
            all_position_directories.append(pos_online_paths)
            continuous_time_directories.append(dataset.get_continuous_time())
        return all_position_directories, continuous_time_directories

    def get_positions(self):
        return [
            MultiThreadDataIterator(
                PosDataManager(directories=[position_directory]))
            for position_directory in self.all_position_directories
        ]

    def get_columns_labels(self):
        return [
            PosDataManager(
                directories=[position_directory]).get_column_labels_as_string()
            for position_directory in self.all_position_directories
        ]

    def get_timestamps(self):
        return [
            MultiThreadTimestampIterator(
                PosTimestampManager(
                    directories=[position_directory],
                    continuous_time_directories=[continuous_time_directory],
                    convert_timestamps=self.convert_timestamps
                ))
            for position_directory, continuous_time_directory in zip(
                self.all_position_directories,
                self.continuous_time_directories)
        ]
