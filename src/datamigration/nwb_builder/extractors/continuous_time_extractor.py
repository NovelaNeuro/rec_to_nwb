from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class ContinuousTimeExtractor:
    @staticmethod
    def get_continuous_time_dict_dataset(dataset):
        continuous_time_file = dataset.get_continuous_time()
        continuous_time = readTrodesExtractedDataFile(continuous_time_file)
        return {str(data[0]): float(data[1]) for data in continuous_time['data']}

    @staticmethod
    def get_continuous_time_dict_file(file):
        continuous_time = readTrodesExtractedDataFile(file)
        return {str(data[0]): float(data[1]) for data in continuous_time['data']}
