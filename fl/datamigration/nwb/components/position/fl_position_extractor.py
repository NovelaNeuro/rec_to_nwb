from fl.datamigration.exceptions.missing_data_exception import MissingDataException
from fl.datamigration.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from fl.datamigration.nwb.components.iterator.multi_thread_timestamp_iterator import MultiThreadTimestampIterator
from fl.datamigration.nwb.components.position.pos_data_manager import PosDataManager
from fl.datamigration.nwb.components.position.pos_timestamp_manager import PosTimestampManager
from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlPositionExtractor:
    def __init__(self, datasets):
        self.datasets = datasets
        self.all_pos, self.continuous_time = self.__extract_data()

    def __extract_data(self):
        validate_parameters_not_none(
            class_name=__name__,
            args=[self.datasets],
            args_name=[NameExtractor.extract_name(self.__init__)[1]]
        )
        all_pos = []
        continuous_time = []
        for dataset in self.datasets:
            data_from_current_dataset = [
                dataset.get_data_path_from_dataset('pos') + pos_file for pos_file in
                dataset.get_all_data_from_dataset('pos') if
                (pos_file.endswith('.pos_online.dat'))]
            if data_from_current_dataset is None or dataset.get_continuous_time() is None:
                raise MissingDataException(
                    'Incomplete data in dataset '
                    + str(dataset.name)
                    + 'missing continuous time file')
            all_pos.append(data_from_current_dataset)
            continuous_time.append(dataset.get_continuous_time())
        return all_pos, continuous_time

    def get_position(self):
        pos_data = PosDataManager(directories=self.all_pos)
        return MultiThreadDataIterator(pos_data)

    def get_timestamps(self):
        pos_timestamp_manager = PosTimestampManager(
            directories=self.all_pos,
            continuous_time_directories=self.continuous_time)
        return MultiThreadTimestampIterator(pos_timestamp_manager)
