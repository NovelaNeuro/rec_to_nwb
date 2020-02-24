from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb_builder.iterators.data_iterator_1_dim import DataIterator1D
from src.datamigration.nwb_builder.iterators.data_iterator_2_dim import DataIterator2D
from src.datamigration.nwb_builder.managers.mda_data_manager import MdaDataManager
from src.datamigration.nwb_builder.managers.mda_timestamp_manager import MdaTimestampDataManager
from src.datamigration.nwb_builder.mda_content import MdaContent


class MdaExtractor:

    def __init__(self, datasets):
        self.datasets = datasets

        self.mda_data = []
        self.timestamps = []
        self.continuous_time = []

    def get_mda_data(self):
        self.__extract_data()

        mda_timestamp_data_manager = MdaTimestampDataManager(
            directories=self.timestamps,
            continuous_time_directories=self.continuous_time
        )
        mda_data_manager = MdaDataManager(self.mda_data)
        data_iterator = DataIterator2D(mda_data_manager)
        data_iterator_1d = DataIterator1D(mda_timestamp_data_manager)

        return MdaContent(data_iterator, data_iterator_1d)

    def __extract_data(self):
        for dataset in self.datasets:
            data_from_current_dataset = self.__get_data_from_current_dataset(dataset)

            self.__check_if_data_exist(data_from_current_dataset, dataset)
            self.__add_data(data_from_current_dataset, dataset)

    @staticmethod
    def __get_data_from_current_dataset(dataset):
        return [dataset.get_data_path_from_dataset('mda') + mda_file for mda_file in
                dataset.get_all_data_from_dataset('mda') if
                (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]

    @staticmethod
    def __check_if_data_exist(data_from_current_dataset, dataset):
        if (data_from_current_dataset is None
                or dataset.get_mda_timestamps() is None
                or dataset.get_continuous_time() is None):
            raise MissingDataException("Incomplete data in dataset " + str(dataset.name) + ", missing mda files")

    def __add_data(self, data_from_current_dataset, dataset):
        self.mda_data.append(data_from_current_dataset)
        self.timestamps.append([dataset.get_mda_timestamps()])
        self.continuous_time.append(dataset.get_continuous_time())
