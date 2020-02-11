from src.datamigration.exceptions.missing_data_exception import MissingDataException
from src.datamigration.nwb_builder.nwb_builder_tools.binary_data import MdaData, MdaTimestamps
from src.datamigration.nwb_builder.nwb_builder_tools.data_iterator import DataIterator, DataIterator1D
from src.datamigration.nwb_builder.others.mda_content import MdaContent


# ToDo Is it SOLID?
# Should be: extract here and manager to get MdaContent


class MdaExtractor:

    def __init__(self, datasets):
        self.datasets = datasets
        self.mda_data = []
        self.timestamps = []
        self.continuous_time = []

    def get_mda_data(self):
        for dataset in self.datasets:
            data_from_current_dataset = [dataset.get_data_path_from_dataset('mda') + mda_file for mda_file in
                                         dataset.get_all_data_from_dataset('mda') if
                                         (mda_file.endswith('.mda') and not mda_file.endswith('timestamps.mda'))]
            if (data_from_current_dataset is None
                    or dataset.get_mda_timestamps() is None
                    or dataset.get_continuous_time() is None):
                raise MissingDataException("Incomplete data in dataset " + str(dataset.name) + ", missing mda files")

            self.mda_data.append(data_from_current_dataset)
            self.timestamps.append(dataset.get_mda_timestamps())
            self.continuous_time.append(dataset.get_continuous_time())

        data = MdaData(self.mda_data)
        extracted_mda = DataIterator(data)
        timestamps = MdaTimestamps(directories=[self.timestamps], continuous_time_directories=self.continuous_time)
        extracted_timestamps = DataIterator1D(timestamps)

        return MdaContent(extracted_mda, extracted_timestamps)
