from rec_to_nwb.processing.exceptions.missing_data_exception import MissingDataException
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_data_iterator import MultiThreadDataIterator
from rec_to_nwb.processing.nwb.components.iterator.multi_thread_timestamp_iterator import MultiThreadTimestampIterator
from rec_to_nwb.processing.nwb.components.mda.mda_content import MdaContent
from rec_to_nwb.processing.nwb.components.mda.mda_data_manager import MdaDataManager
from rec_to_nwb.processing.nwb.components.mda.mda_timestamp_manager import MdaTimestampDataManager

class FlMdaExtractor:

    def __init__(self, datasets, conversion):
        self.datasets = datasets
        # the conversion is to volts, so we multiple by 1e6 to change to uV
        self.raw_to_uv = float(conversion) * 1e6
        
    def get_data(self):
        mda_data_files, timestamp_files, continuous_time_files = self.__extract_data_files()
        mda_timestamp_data_manager = MdaTimestampDataManager(
            directories=timestamp_files,
            continuous_time_directories=continuous_time_files
        )
        mda_data_manager = MdaDataManager(mda_data_files, self.raw_to_uv)
        # check the number of files and set the number of threads appropriately assuming 32 GB of available RAM
        datalen = [mda_data_manager.get_data_shape(dataset_num)[1] 
                for dataset_num in range(len(mda_data_manager.directories))] 
        if max(datalen) < 3e9: # each file < 3GB samples (2 bytes / sample)
            num_threads = 6
        elif max(datalen) < 6e9:
            num_threads = 3
        else:
            num_threads = 1

        print(f'in FlMdaExtractor: will write {num_threads} files as a chunk')
        data_iterator = MultiThreadDataIterator(mda_data_manager, number_of_threads=num_threads)
        timestamp_iterator = MultiThreadTimestampIterator(mda_timestamp_data_manager)

        return MdaContent(data_iterator, timestamp_iterator)

    def __extract_data_files(self):
        mda_data_files = []
        timestamp_files = []
        continuous_time_files = []

        for dataset in self.datasets:
            data_files_from_single_dataset = self.__extract_data_files_for_single_dataset(dataset)
            mda_data_files.append(data_files_from_single_dataset[0])
            timestamp_files.append(data_files_from_single_dataset[1])
            continuous_time_files.append(data_files_from_single_dataset[2])

        return mda_data_files, timestamp_files, continuous_time_files

    def __extract_data_files_for_single_dataset(self, dataset):
        data_from_current_dataset = self.__get_data_files_from_current_dataset(dataset)

        if not self.__data_exist(data_from_current_dataset, dataset):
            raise MissingDataException("Incomplete data in dataset " + str(dataset.name) + ", missing mda files")

        return data_from_current_dataset, [dataset.get_mda_timestamps()], dataset.get_continuous_time()

    @staticmethod
    def __get_data_files_from_current_dataset(dataset):
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
