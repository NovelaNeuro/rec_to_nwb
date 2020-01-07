import os
import unittest

import src.datamigration.file_scanner as fs

path = os.path.dirname(os.path.abspath(__file__))


class TestFileScanner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_folder = fs.DataScanner(path + '/res/scanner_test/')
        cls.probe_path = path + '/res/probe_test'

    def test_finding_all_datasets(self):
        self.assertEqual(len(self.data_folder.data.values()), 1)
        self.assertEqual(len(self.data_folder.data['alien'].values()), 1)
        self.assertEqual(len(self.data_folder.data['alien']['21251015'].values()), 2)

    def test_finding_all_data_folders(self):
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.1.pos/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('pos'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.DIO/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('DIO'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.LFP/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('LFP'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.mda/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.metadata/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('metadata'))
        # in test data mountain folder is empty so its not uploaded to git
        # self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.mountain/'),
        # self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('mountain'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.spikes/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('spikes'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.time/'),
                         self.data_folder.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('time'))

    def test_number_of_files(self):
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('pos')), 3)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('DIO')), 7)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('LFP')), 4)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('mda')), 4)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('metadata')),
                         1)
        # in test data mountain folder is empty so its not uploaded to git
        # self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('mountain')),
        #                 0)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('spikes')),
                         3)
        self.assertEqual(len(self.data_folder.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('time')),
                         2)

    def test_get_probes(self):
        probes = self.data_folder.get_probes_from_directory(self.probe_path)
        probes.sort()
        self.assertEqual('probe1.yml', probes[0], 'should be probe1.yml')
        self.assertEqual('probe2.yml', probes[1], 'should be probe2.yml')
        self.assertEqual('probe21.yml', probes[2], 'should be probe21.yml')
