import os
from unittest import TestCase

import lf.datamigration.tools.file_scanner as fs

path = os.path.dirname(os.path.abspath(__file__))


class TestFileScanner(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_scanner = fs.DataScanner(
            data_path=path + '/res/scanner_test/',
            animal_name='alien'
        )
        cls.probe_path = path + '/res/probe_test'

    def test_finding_all_datasets(self):
        self.assertEqual(len(self.data_scanner.data.values()), 1)
        self.assertEqual(len(self.data_scanner.data['alien'].values()), 1)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015'].values()), 2)

    def test_finding_all_data_scanners(self):
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.1.pos/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('pos'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.DIO/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('DIO'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.LFP/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('LFP'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.mda/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.metadata/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('metadata'))
        # in test data mountain folder is empty so its not uploaded to git
        # self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.mountain/'),
        # self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('mountain'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.spikes/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('spikes'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.time/'),
                         self.data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('time'))

    def test_number_of_files(self):
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('pos')), 3)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('DIO')), 7)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('LFP')), 4)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('mda')), 4)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('metadata')),
                         1)
        # in test data mountain folder is empty so its not uploaded to git
        # self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('mountain')),
        #                 0)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('spikes')),
                         3)
        self.assertEqual(len(self.data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('time')),
                         2)

    def test_get_probes(self):
        probes = self.data_scanner.get_probes_from_directory(self.probe_path)
        probes.sort()
        self.assertTrue(probes[0].endswith('probe1.yml'))
        self.assertTrue(probes[1].endswith('probe2.yml'))
        self.assertTrue(probes[2].endswith('probe21.yml'))
