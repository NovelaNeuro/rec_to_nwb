import os
import unittest

import pandas as pd
from pynwb.behavior import Position

from src.datamigration.nwb_builder.pos_extractor import POSExtractor

path = os.path.dirname(os.path.abspath(__file__))


class TestPOSMigration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path_to_beans = path + '/res/1.pos_online.dat'
        cls.pos_extractor = POSExtractor(path=cls.path_to_beans)
        cls.position = cls.pos_extractor.get_position()

    def test_reading_pos_extractor(self):
        self.assertIsNotNone(self.pos_extractor)
        self.assertIsInstance(self.pos_extractor, POSExtractor)
        self.assertEqual((32658, 5), pd.DataFrame(self.pos_extractor.pos_online['data']).shape,
                         'Shape should be (32658, 5)')
        self.assertEqual('73', self.pos_extractor.pos_online['threshold'])
        self.assertEqual('0', self.pos_extractor.pos_online['dark'])
        self.assertEqual('20000', self.pos_extractor.pos_online['clockrate'])
        self.assertEqual('1000x1000', self.pos_extractor.pos_online['camera resolution'])
        self.assertEqual('0 pix/cm', self.pos_extractor.pos_online['pixel scale'])
        self.assertEqual('<time uint32><xloc uint16><yloc uint16><xloc2 uint16><yloc2 uint16>',
                         self.pos_extractor.pos_online['fields'])

    def test_reading_position(self):
        """
            In pandas series to take last element you must use .iloc, normal [-1] will crash:
             self.assertEqual(570, self.position['Fields'].data[1].iloc[-1])
        """
        self.assertIsNotNone(self.position)
        self.assertIsInstance(self.position, Position)
        self.assertEqual('no comments', self.position['Fields'].comments)
        self.assertEqual(1.0, self.position['Fields'].conversion)
        # ToDo too much data self.assertEqual([]], self.position['Fields'].data)
        self.assertEqual(0, self.position['Fields'].data[0][0])
        self.assertEqual(570, self.position['Fields'].data[1].iloc[-1])
        self.assertEqual('no description', self.position['Fields'].description)
        self.assertEqual(1, self.position['Fields'].interval)
        self.assertEqual('Description defining what the zero-position is', self.position['Fields'].reference_frame)
        self.assertEqual(-1.0, self.position['Fields'].resolution)
        # ToDo too much data self.assertEqual([], self.position['Fields'].timestamps)
        self.assertEqual(1436261, self.position['Fields'].timestamps[0])
        self.assertEqual(23207135, self.position['Fields'].timestamps[-1])
        self.assertEqual('seconds', self.position['Fields'].timestamps_unit)
        self.assertEqual('meters', self.position['Fields'].unit)
