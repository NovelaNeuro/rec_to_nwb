import os
import unittest

from testfixtures import should_raise

from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_files_manager import FlAssociatedFilesManager
path = os.path.dirname(os.path.abspath(__file__))


class TestFlAssociatedFilesManager(unittest.TestCase):

    def setUp(self):
        self.fl_associated_files_manager = FlAssociatedFilesManager(
            [
             {'name': 'test1_file',
              'description': 'test1 description of the file',
              'path': path + '/../res/test_text_files/test1_file',
              'task_epochs': '1,2'
              }
             ,
             {'name': 'test2_file',
              'description': 'test2 description of the file',
              'path': path + '/../res/test_text_files/test2_file',
              'task_epochs': '1,2'
              }
            ]
        )

    def test_fl_associated_files_manager_get_fl_associated_files_successfully(self):
        fl_associated_files = self.fl_associated_files_manager.get_fl_associated_files()

        self.assertEqual(2, len(fl_associated_files))
        self.assertEqual('test1_file', fl_associated_files[0].name)
        self.assertEqual('test2 description of the file', fl_associated_files[1].description)
        self.assertEqual('some test text inside from test1_file', fl_associated_files[0].content)

    @should_raise(TypeError)
    def test_fl_associated_files_manager_fail_none_param_associated_files_metadata(self):
        fl_associated_files_manager = FlAssociatedFilesManager(
            None
        )

    def test_if_associated_files_empty(self):
        fl_associated_files_manager = FlAssociatedFilesManager(
            []
        )
