import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile


class DioFiles:

    @staticmethod
    def get_dio_dict(directory):
        dio_dict = {}
        files = os.listdir(directory)
        files.sort()
        for file in files:
            if file.endswith('.dat'):
                split_filename = file.split('.')
                dio_dict[split_filename[-2].split('_')[1]] = file
        return dio_dict
