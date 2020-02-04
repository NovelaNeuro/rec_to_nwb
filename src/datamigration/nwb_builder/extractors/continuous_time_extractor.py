from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class ContinuousTimeExtractor:
    @staticmethod
    def get_continuous_time_dict(dataset):
        continuous_time_file = dataset.get_continuous_time()
        continuous_time = readTrodesExtractedDataFile(continuous_time_file)
        continuous_time_dict = {str(data[0]): float(data[1]) for data in continuous_time['data']}
        return continuous_time_dict
