import unittest
from pathlib import Path

import numpy as np
from pynwb.behavior import BehavioralEvents

from src.datamigration.nwb_builder.creators.dio_creator import DioCreator
from src.datamigration.nwb_builder.extractors.dio_extractor import DioExtractor
from src.datamigration.nwb_builder.managers.dio_manager import DioManager
from src.datamigration.nwb_builder.nwb_metadata import NWBMetadata
from src.datamigration.tools.file_scanner import Dataset

path = Path(__file__).parent.parent
path.resolve()


# @unittest.skip('DIO test require real dio files')
class TestDio(unittest.TestCase):

    def setUp(self):
        nwbmetadata = NWBMetadata(str(path) + '/datamigration/res/metadata.yml',
                                  [str(path) + '/datamigration/res/probe1.yml',
                                   str(path) + '/datamigration/res/probe2.yml',
                                   str(path) + '/datamigration/res/probe3.yml'
                                   ])
        self.metadata = nwbmetadata.metadata

    def test_dio_extractor(self):
        extractor = DioExtractor([self.create_test_dataset()], self.metadata)
        timeseries = extractor.get_dio()
        print(timeseries[0])
        self.assertTrue(1)

    def test_dio_creator(self):
        creator = DioCreator()
        behavioral_event = BehavioralEvents(name='test', )
        test_timeseries = {}
        test_data = np.ndarray((10,), dtype="int16")
        test_timestamps = np.ndarray((10,), dtype="int16")
        test_timeseries["name"] = "test_name"
        test_timeseries["description"] = "test_description"
        for i in range(10):
            test_data[i] = i
            test_timestamps[i] = i
        test_timeseries["dio_timeseries"] = test_data
        test_timeseries["dio_timestamps"] = test_timestamps
        creator.create_dio_time_series(behavioral_event, [test_timeseries])
        for i in range(10):
            self.assertEqual(behavioral_event.__getitem__("test").data[i], test_data[i])
            self.assertEqual(behavioral_event.__getitem__("test").timestamps[i], test_timestamps[i])

    def test_dio_manager(self):
        dataset = self.create_test_dataset()
        manager = DioManager(metadata=self.metadata)
        behavioral_events = manager.get_behavioral_events()
        dio_1 = manager.get_extracted_dio(dataset, "Din1")
        dio_data = [(1367266, 0), (9599570, 1), (9603169, 0)]
        self.assertEqual(behavioral_events[0]["name"], "Din1")
        self.assertEqual(behavioral_events[1]["name"], "Din2")
        for i in range(3):
            for j in range(2):
                self.assertEqual(dio_1["data"][i][j], dio_data[i][j])

    def create_test_dataset(self):
        dataset = Dataset('test_dataset')
        dataset.add_data_to_dataset(str(path) + '/datamigration/res/dio_test/', 'DIO')
        dataset.add_data_to_dataset(str(path) + '/test_data/beans/preprocessing/20190718/20190718_beans_01_s1.time/',
                                    'time')
        return dataset
