from unittest import TestCase
from unittest.mock import patch, Mock

from testfixtures import should_raise

from fl.datamigration.exceptions.none_param_exception import NoneParamException
from fl.datamigration.nwb.components.epochs.fl_epochs import FlEpochs
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
        mock1 = Mock(spec=Dataset)
        mock1.name = 'mock1'
        mock2 = Mock(spec=Dataset)
        mock2.name = 'mock2'
        datasets = [mock1, mock2]
        metadata = {'tasks': [{'task_name': 'task1'}, {'task_name': 'task2'}]}

        fl_epochs_manager = FlEpochsManager(
            datasets,
            metadata
        )
        fl_epochs = fl_epochs_manager.get_epochs()

        self.assertIsInstance(fl_epochs, FlEpochs)
        self.assertEqual(2, len(fl_epochs.session_start_times))
        self.assertEqual(2, len(fl_epochs.session_end_times))
        self.assertEqual(2, len(fl_epochs.tags))
        self.assertEqual(2, len(fl_epochs.tasks))

    @should_raise(NoneParamException)
    def test_get_epochs_fails_due_to_None_param(self):
        metadata = {'tasks': [{'task_name': 'task1'}, {'task_name': 'task2'}]}
        FlEpochsManager(
            None,
            metadata
        )



