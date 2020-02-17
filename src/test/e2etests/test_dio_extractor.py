import unittest
from pathlib import Path

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip('DIO test requires real dio files')
class TestDioExtractor(unittest.TestCase):

    def setUp(self):
        nwbmetadata = MetadataManager(str(path) + '/datamigration/res/metadata.yml',
                                      [str(path) + '/datamigration/res/probe1.yml',
                                       str(path) + '/datamigration/res/probe2.yml',
                                       str(path) + '/datamigration/res/probe3.yml'
                                       ])
        self.metadata = nwbmetadata.metadata

        self.filtered_dio_files = [str(path) + '/datamigration/res/dio_test/20190718_beans_01_s1.dio_Din1.dat',
                                   str(path) + '/datamigration/res/dio_test/20190718_beans_01_s1.dio_Din2.dat']

        continuous_time_path = str(
            path) + '/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/20190718_beans_01_s1.continuoustime.dat'
        self.continuous_time_dict = ContinuousTimeExtractor.get_continuous_time_dict_file(continuous_time_path)

    def test_dio_extractor(self):
        dio_extractor = DioExtractor(self.filtered_dio_files, [self.continuous_time_dict])
        dataset_dio_data = dio_extractor.get_dio()
        self.assertEqual(list, type(dataset_dio_data))
        self.assertEqual(len(self.filtered_dio_files), len(dataset_dio_data))

    # def test_dio_creator(self):
    #     creator = DioCreator()
    #     behavioral_event = BehavioralEvents(name='test', )
    #     test_timeseries = {}
    #     test_data = np.ndarray((10,), dtype="int16")
    #     test_timestamps = np.ndarray((10,), dtype="int16")
    #     test_timeseries["name"] = "test_name"
    #     test_timeseries["description"] = "test_description"
    #     for i in range(10):
    #         test_data[i] = i
    #         test_timestamps[i] = i
    #     test_timeseries["dio_timeseries"] = test_data
    #     test_timeseries["dio_timestamps"] = test_timestamps
    #     creator.create_dio_time_series(behavioral_event, [test_timeseries])
    #     for i in range(10):
    #         self.assertEqual(behavioral_event.__getitem__("test").data[i], test_data[i])
    #         self.assertEqual(behavioral_event.__getitem__("test").timestamps[i], test_timestamps[i])
    #
    # def test_dio_manager(self):
    #     dataset = self.create_test_dataset()
    #     dio_files = DioFiles()
    #     dio_1 = dio_files.get_dio_dict(dataset.get_data_path_from_dataset('DIO'))
    #     dio_data_2 = [(1367266, 0), (9599570, 1), (9603169, 0)]
    #
    #     dio_data = readTrodesExtractedDataFile(dataset.get_data_path_from_dataset('DIO') + dio_1["Din1"])
    #     for i in range(3):
    #         for j in range(2):
    #             self.assertEqual(dio_data["data"][i][j], dio_data_2[i][j])
    #
