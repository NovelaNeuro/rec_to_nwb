import os
import unittest

from fl.datamigration.nwb.components.associated_files.fl_associated_files_manager import FlAssociatedFilesManager
path = os.path.dirname(os.path.abspath(__file__))


class TestFlAssociatedFilesManager(unittest.TestCase):

    def setUp(self):
        self.fl_associated_files_manager = FlAssociatedFilesManager([
            (path + '/../../datamigration/res/test_text_files/test1_file'),
            (path + '/../../datamigration/res/test_text_files/test2_file')
            ],
            [{'name': 'test1_file',
             'description': 'test1 description of the file'},
             {'name': 'test2_file',
              'description': 'test2 description of the file'}
             ]
        )

    def test_get_fl_associated_files_correct_build(self):
        fl_associated_files = self.fl_associated_files_manager.get_fl_associated_files()
        self.assertEqual(2, len(fl_associated_files))
        self.assertEqual('test1_file', fl_associated_files[0].name)
        self.assertEqual('test2 description of the file', fl_associated_files[1].description)
        self.assertEqual('some test text inside from test1_file', fl_associated_files[0].content)
