import unittest
from pathlib import Path

from src.datamigration.nwb_builder.managers.dio_manager import DioManager
from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = Path(__file__).parent.parent
path.resolve()


class TestDioManager(unittest.TestCase):

    def setUp(self):
        nwbmetadata = MetadataManager(str(path) + '/datamigration/res/metadata.yml', [])
        metadata = nwbmetadata.metadata['behavioral_events']
        self.dio_manager = DioManager([str(path) + '/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.DIO',
                                       str(path) + '/test_data/beans/preprocessing/20190718/20190718_beans_02_r1.DIO',
                                       str(path) + '/test_data/beans/preprocessing/20190718/20190718_beans_03_s2.DIO',
                                       str(path) + '/test_data/beans/preprocessing/20190718/20190718_beans_04_r2.DIO'],
                                      dio_metadata=metadata)

    def test_get_dio_files(self):
        self.assertEqual(4, len(self.dio_manager.get_dio_files()))
        self.assertEqual(len(self.dio_manager.get_dio_files()[0]), len(self.dio_manager.dio_metadata))

    def test_merge_dio_data(self):
        test_list_to_merge = [{'Din1': [(1, 11), (1, 11)], 'Din2': [(2, 22), (2, 22), (2, 22)]},
                              {'Din1': [(1, 11), (1, 11)], 'Din2': [(2, 22), (2, 22)]}]
        merged_data = self.dio_manager.merge_dio_data(test_list_to_merge)
        self.assertEqual({'Din1': [(1, 11), (1, 11), (1, 11), (1, 11)],
                          'Din2': [(2, 22), (2, 22), (2, 22), (2, 22), (2, 22)]},
                         merged_data)
