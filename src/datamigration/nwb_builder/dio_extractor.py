import os

from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

log = open('log.txt', 'w')

for index in range(32):
    index += 1
    d_in = readTrodesExtractedDataFile('C:/Users/wmery/PycharmProjects/LorenFranksDataMigration/src/test/test_data/jaq/preprocessing/20190911/20190911_jaq_01_s1.DIO/20190911_jaq_01_s1.dio_Din'+str(index)+'.dat')
    log.write(str(d_in))
    log.write(str(index))


class DioExtractor:

    def __init__(self, path):
        self.path = path
        pass

    def get_dio(self):
        dio_names = [dio_file for dio_file in os.listdir(self.path) if
                     (dio_file.endswith('.dio') and not dio_file.endswith('timestamps.dio'))]
        dio_files = []
        for dio_file in dio_names:
            dio_files.append(self.path + dio_file)
