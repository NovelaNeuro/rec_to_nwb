import os
import unittest

from ndx_fl_novela.associated_files import AssociatedFiles

from fl.datamigration.nwb.components.associated_files.associated_files_creator import AssociatedFilesCreator
from fl.datamigration.nwb.components.associated_files.fl_associated_file import FlAssociatedFile

path = os.path.dirname(os.path.abspath(__file__))


class TestFlAssociatedFilesCreator(unittest.TestCase):

    def setUp(self):
        fl_associated_files = [
            FlAssociatedFile('test_name1', 'test description 1', 'test content 1'),
            FlAssociatedFile('test_name2', 'test description 2', 'test content 2')]
        self.associated_files_creator = AssociatedFilesCreator(fl_associated_files)

    def test_fl_associated_files_creator_correct_create(self):
        associated_files = self.associated_files_creator.create()
        self.assertEqual(2, len(associated_files))
        self.assertIsInstance(associated_files[0], AssociatedFiles)
        self.assertEqual('test_name1', associated_files[0].name)
        self.assertEqual('test description 2', associated_files[1].fields['description'])
        self.assertEqual('test content 2', associated_files[1].fields['content'])
