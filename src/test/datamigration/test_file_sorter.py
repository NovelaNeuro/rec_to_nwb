import unittest

from src.datamigration.file_sorter import FileSorter


class TestFilenameSorter(unittest.TestCase):
    def setUp(self):
        self.filenames_to_sort = ['name1', 'name11', 'name10', 'name2', 'name21']
        self.correct_order = ['name1', 'name2', 'name10', 'name11', 'name21']
        self.file_sorter = FileSorter()

    def test_filename_sorting(self):
        self.assertEqual(self.file_sorter.sort_filenames(self.filenames_to_sort), self.correct_order)
