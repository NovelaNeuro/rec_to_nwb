from unittest import TestCase
from unittest.mock import patch, Mock

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.epochs.fl_epochs_extractor import FlEpochsExtractor
from fl.datamigration.nwb.components.epochs.fl_epochs_manager import FlEpochsManager
from fl.datamigration.tools.dataset import Dataset


class TestFlElEpochsManager(TestCase):

    @staticmethod
    def fake_extract_epochs(*args, **kwargs):
        return [11111111.0, 222222222.0], [333333333.0, 4444444444.0]

    @staticmethod
    def fake_get_continuous_time(*args, **kwargs):
        return ['file1', 'file2']

    @patch.object(Dataset, 'get_continuous_time', new=fake_get_continuous_time)
    @patch.object(FlEpochsExtractor, 'extract_epochs', new=fake_extract_epochs)
    def test_get_epochs_returnCorrectData_successfully(self):
        dataset_1_mock = Mock(spec=Dataset)
        dataset_1_mock.name = 'mock1'
        dataset_2_mock = Mock(spec=Dataset)
        dataset_2_mock.name = 'mock2'
        datasets = [dataset_1_mock, dataset_2_mock]
        metadata = {'tasks': [{'task_name': 'task1'}, {'task_name': 'task2'}]}

        fl_epochs_manager = FlEpochsManager(
            datasets,
            metadata
        )
        fl_epochs = fl_epochs_manager.get_epochs()

        self.assertEqual(2, len(fl_epochs.session_start_times))
        self.assertEqual(2, len(fl_epochs.session_end_times))
        self.assertEqual(2, len(fl_epochs.tags))
        self.assertEqual(2, len(fl_epochs.tasks))
        self.assertEqual(11111111.0, fl_epochs.session_start_times[0])
        self.assertEqual(4444444444.0, fl_epochs.session_end_times[1])
        self.assertEqual('task1', fl_epochs.tasks[0])
        self.assertEqual('mock1', fl_epochs.tags[0])

    @should_raise(NoneParamException)
    def test_get_epochs_fails_due_to_None_param(self):
        metadata = {'tasks': [{'task_name': 'task1'}, {'task_name': 'task2'}]}
        FlEpochsManager(
            None,
            metadata
        )



