from unittest import TestCase
from unittest.mock import patch, Mock

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_manager import FlEpochsManager
from rec_to_nwb.processing.tools.dataset import Dataset


class TestFlElEpochsManager(TestCase):

    def setUp(self):
        dataset_1_mock = Mock(spec=Dataset)
        dataset_1_mock.name = 'mock1'
        dataset_2_mock = Mock(spec=Dataset)
        dataset_2_mock.name = 'mock2'
        self.datasets = [dataset_1_mock, dataset_2_mock]

    @staticmethod
    def fake_extract_epochs(*args, **kwargs):
        return [11111111.0, 222222222.0], [333333333.0, 4444444444.0]

    @staticmethod
    def fake_get_continuous_time(*args, **kwargs):
        return ['file1', 'file2']

    @patch.object(Dataset, 'get_continuous_time', new=fake_get_continuous_time)
    @patch.object(FlEpochsExtractor, 'extract_epochs', new=fake_extract_epochs)
    def test_get_epochs_returnCorrectData_successfully(self):
        fl_epochs_manager = FlEpochsManager(
            self.datasets
        )
        fl_epochs = fl_epochs_manager.get_epochs()

        self.assertEqual(2, len(fl_epochs.session_start_times))
        self.assertEqual(2, len(fl_epochs.session_end_times))
        self.assertEqual(2, len(fl_epochs.tags))
        self.assertEqual(11111111.0, fl_epochs.session_start_times[0])
        self.assertEqual(4444444444.0, fl_epochs.session_end_times[1])
        self.assertEqual('mock1', fl_epochs.tags[0])

    @should_raise(NoneParamException)
    def test_get_epochs_fails_due_to_None_param(self):
        FlEpochsManager(
            None
        )


