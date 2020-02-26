from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb.components.iterator.single_thread_data_iterator import SingleThreadDataIterator2D
from src.datamigration.nwb.components.iterator.single_thread_timestamp_iterator import SingleThreadTimestampIterator1D
from src.datamigration.nwb.components.mda.mda_content import MdaContent
from src.datamigration.nwb.components.mda.mda_data_manager import MdaDataManager
from src.datamigration.nwb.components.mda.mda_timestamp_manager import MdaTimestampDataManager


class LfMdaExtractor:

    def __init__(self, datasets):
        self.datasets = datasets

    def get_data(self):
        mda_data, timestamps, continuous_time = self.__extract_data()
        mda_timestamp_data_manager = MdaTimestampDataManager(
            directories=timestamps,
            continuous_time_directories=continuous_time
        )
        mda_data_manager = MdaDataManager(mda_data)
        data_iterator_2d = SingleThreadDataIterator2D(mda_data_manager)
        data_iterator_1d = SingleThreadTimestampIterator1D(mda_timestamp_data_manager)

        return MdaContent(data_iterator_2d, data_iterator_1d)

    def __extract_data(self):
        mda_data = []
        timestamps = []
        continuous_time = []

        for dataset in self.datasets:
            data_from_single_dataset = self.__extract_data_for_single_dataset(dataset)
            mda_data.append(data_from_single_dataset[0])
            timestamps.append(data_from_single_dataset[1])
            continuous_time.append(data_from_single_dataset[2])

        return mda_data, timestamps, continuous_time

    def __extract_data_for_single_dataset(self, dataset):
        data_from_current_dataset = self.__get_data_from_current_dataset(dataset)

        if not self.__data_exist(data_from_current_dataset, dataset):
            raise MissingDataException("Incomplete data in dataset " + str(dataset.name) + ", missing mda files")

        return data_from_current_dataset, [dataset.get_mda_timestamps()], dataset.get_continuous_time()

    @staticmethod
    def __get_data_from_current_dataset(dataset):
        return [dataset.get_data_path_from_dataset('mda') + mda_file for mda_file in
                dataset.get_all_data_from_dataset('mda') if
                (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]

    @staticmethod
    def __data_exist(data_from_current_dataset, dataset):
        if (data_from_current_dataset is None
                or dataset.get_mda_timestamps() is None
                or dataset.get_continuous_time() is None):
            return False
        return True
