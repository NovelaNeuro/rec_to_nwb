from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class DioManager:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_behavioral_events(self):
        all_dio_timeseries = self.metadata['behavioral_events']
        return all_dio_timeseries

    def get_extracted_dio(self, dataset, name):
        dataset = dataset
        dio_set = dataset.get_all_data_from_dataset('DIO')
        dio_path = dataset.get_data_path_from_dataset('DIO')
        for dio_file in dio_set:
            if name + '.' in dio_file:
                dio_data = readTrodesExtractedDataFile(dio_path + dio_file)
                return dio_data
        return None

    @staticmethod
    def get_continuous_time_dict(dataset):
        continuous_time_file = dataset.get_continuous_time()
        continuous_time = readTrodesExtractedDataFile(continuous_time_file)
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        return continuous_time_dict
