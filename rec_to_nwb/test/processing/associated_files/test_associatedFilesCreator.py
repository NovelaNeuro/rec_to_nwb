import os
import unittest

from ndx_franklab_novela.associated_files import AssociatedFiles

from rec_to_nwb.processing.nwb.components.associated_files.associated_files_creator import AssociatedFilesCreator
from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_file import FlAssociatedFile

path = os.path.dirname(os.path.abspath(__file__))


class TestFlAssociatedFilesCreator(unittest.TestCase):

    def setUp(self):
        self.fl_associated_files = [
            FlAssociatedFile('test_name1', 'test description 1', 'test content 1', '1,2'),
            FlAssociatedFile('test_name2', 'test description 2', 'test content 2', '1,2')
        ]
        self.associated_files_creator = AssociatedFilesCreator()

    def test_fl_associated_files_creator_create_successfully(self):
        associated_files = [
            self.associated_files_creator.create(fl_associated_file)
            for fl_associated_file in self.fl_associated_files
        ]

        self.assertEqual(2, len(associated_files))
        self.assertIsInstance(associated_files[0], AssociatedFiles)
        self.assertEqual('test_name1', associated_files[0].name)
        self.assertEqual('test description 2', associated_files[1].fields['description'])
        self.assertEqual('test content 2', associated_files[1].fields['content'])
