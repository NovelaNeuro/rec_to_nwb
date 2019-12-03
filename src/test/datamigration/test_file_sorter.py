import unittest

from src.datamigration.file_sorter import FileSorter


class TestFilenameSorter(unittest.TestCase):
    def setUp(self):
        self.strings_to_sort = ['name1', 'name11', 'name10', 'name2', 'name21']
        self.correct_order_of_strings = ['name1', 'name2', 'name10', 'name11', 'name21']
        self.filenames_to_sort = ['20190718_beans_01_s1.nt' + str(i) + '.mda' for i in range(1, 64)]
        self.file_sorter = FileSorter()
        self.sorted_strings = self.file_sorter.sort_filenames(self.strings_to_sort)
        self.sorted_filenames = self.file_sorter.sort_filenames(self.filenames_to_sort)


    def test_filename_sorting(self):
        self.assertEqual(self.sorted_strings, self.correct_order_of_strings)
        self.assertEqual(self.sorted_filenames[1], '20190718_beans_01_s1.nt2.mda')
        self.assertEqual(self.sorted_filenames[9], '20190718_beans_01_s1.nt10.mda')
        self.assertEqual(self.sorted_filenames[18], '20190718_beans_01_s1.nt19.mda')
        self.assertEqual(self.sorted_filenames[19], '20190718_beans_01_s1.nt20.mda')
