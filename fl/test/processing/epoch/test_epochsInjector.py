from datetime import datetime
from unittest import TestCase

from dateutil.tz import tzlocal
from pynwb import NWBFile

from fl.processing.nwb.components.epochs.epochs_injector import EpochsInjector
from fl.processing.nwb.components.epochs.fl_epochs import FlEpochs


class TestEpochInjector(TestCase):

    def setUp(self):
        self.fl_epochs = FlEpochs([1234567.0, 435634.0], [345453.0, 213465.0], ['01_s1', '02_r2'])
        self.nwb_content = NWBFile(
            session_description='None',
            identifier='NWB1',
            session_start_time=datetime(2017, 4, 3, 11, tzinfo=tzlocal()),
            file_create_date=datetime(2017, 4, 15, 12, tzinfo=tzlocal())
        )

    def test_injection(self):
        EpochsInjector.inject(self.fl_epochs, self.nwb_content)
        self.assertIsNotNone(self.nwb_content.epochs)
        self.assertEqual(1234567.0, self.nwb_content.epochs[0, 1])
        self.assertEqual(2, len(self.nwb_content.epochs))
        self.assertEqual(4, len(self.nwb_content.epochs.fields))
