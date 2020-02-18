import unittest
from pathlib import Path

from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager
from src.datamigration.nwb_builder.managers.metadata_manager import MetadataManager

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip('unnecesary test now')
class TestDioManager(unittest.TestCase):

    def setUp(self):
        nwbmetadata = MetadataManager(str(path) + '/datamigration/res/metadata.yml', [])
        dio_directory = (str(path) + '/datamigration/res/dio_test')
        metadata = nwbmetadata.metadata['behavioral_events']

        continuous_time_path = str(path) + \
                               '/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/20190718_beans_01_s1.continuoustime.dat'
        self.continuous_time_dicts = [ContinuousTimeExtractor.get_continuous_time_dict_file(continuous_time_path)]

        self.dio_manager = DioManager(directories=[dio_directory],
                                      dio_metadata=metadata,
                                      continuous_time_dicts=self.continuous_time_dicts)

    def test_dio_extractor(self):
        dio_data = self.dio_manager.get_dio()
        self.assertIsNotNone(dio_data)
        self.assertEqual(1, len(dio_data))
