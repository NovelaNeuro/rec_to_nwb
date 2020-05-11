import os
from unittest import TestCase

from testfixtures import should_raise

from rec_to_nwb.processing.exceptions.none_param_exception import NoneParamException
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.tools.data_scanner import DataScanner

path = os.path.dirname(os.path.abspath(__file__))


class TestDataScanner(TestCase):

    def test_data_scanner_find_all_datasets_with_None_date_param_successfully(self):
        data_scanner = DataScanner(
            data_path=path + '/res/scanner_test/',
            animal_name='alien',
            nwb_metadata = MetadataManager(
                metadata_path=str(path) + '/res/metadata.yml',
                probes_paths=[
                    str(path) + '/res/probe1.yml',
                    str(path) + '/res/probe2.yml',
                    str(path) + '/res/probe3.yml'
                ]
            )
        )
        data_scanner.extract_data_from_all_dates_folders()

        self.assertEqual(len(data_scanner.data.values()), 1)
        self.assertEqual(len(data_scanner.data['alien'].values()), 1)
        self.assertEqual(len(data_scanner.data['alien']['21251015'].values()), 2)

    def test_data_scanner_find_all_data_with_None_date_param_successfully(self):
        data_scanner = DataScanner(
            data_path=path + '/res/scanner_test/',
            animal_name='alien',
            nwb_metadata=MetadataManager(
                metadata_path=str(path) + '/res/metadata.yml',
                probes_paths=[
                    str(path) + '/res/probe1.yml',
                    str(path) + '/res/probe2.yml',
                    str(path) + '/res/probe3.yml'
                ]
            )
        )
        data_scanner.extract_data_from_all_dates_folders()

        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.1.pos/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('pos'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.DIO/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('DIO'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.LFP/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('LFP'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.mda/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('mda'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.metadata/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('metadata'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.spikes/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('spikes'))
        self.assertEqual((path + '/res/scanner_test/alien/preprocessing/21251015/21251015_alien_01_s1.time/'),
                         data_scanner.data['alien']['21251015']['01_s1'].get_data_path_from_dataset('time'))

    def test_data_scanner_return_all_data_with_None_date__successfully(self):
        data_scanner = DataScanner(
            data_path=path + '/res/scanner_test/',
            animal_name='alien',
            nwb_metadata=MetadataManager(
                metadata_path=str(path) + '/res/metadata.yml',
                probes_paths=[
                    str(path) + '/res/probe1.yml',
                    str(path) + '/res/probe2.yml',
                    str(path) + '/res/probe3.yml'
                ]
            )
        )
        data_scanner.extract_data_from_all_dates_folders()

        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('pos')), 3)
        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('DIO')), 7)
        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('LFP')), 4)
        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('mda')), 4)
        self.assertEqual(
            len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('metadata')),
            1)
        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('spikes')),
                         3)
        self.assertEqual(len(data_scanner.data['alien']['21251015']['01_s1'].get_all_data_from_dataset('time')),
                         2)

    def test_data_scanner_find_all_probes_file_with_None_date_param_successfully(self):
        data_scanner = DataScanner(
            data_path=path + '/res/scanner_test/',
            animal_name='alien',
            nwb_metadata=MetadataManager(
                metadata_path=str(path) + '/res/metadata.yml',
                probes_paths=[
                    str(path) + '/res/probe1.yml',
                    str(path) + '/res/probe2.yml',
                    str(path) + '/res/probe3.yml'
                ]
            )
        )
        probe_path = path + '/res/probe_test'

        probes = data_scanner.get_probes_from_directory(probe_path)
        probes.sort()
        self.assertTrue(probes[0].endswith('probe1.yml'))
        self.assertTrue(probes[1].endswith('probe2.yml'))
        self.assertTrue(probes[2].endswith('probe21.yml'))

    @should_raise(NoneParamException)
    def test_data_scanner_failed_due_to_None_parameter(self):
        DataScanner(
            data_path=None,
            animal_name='alien',
            nwb_metadata=MetadataManager(
                metadata_path=str(path) + '/res/metadata.yml',
                probes_paths=[
                    str(path) + '/res/probe1.yml',
                    str(path) + '/res/probe2.yml',
                    str(path) + '/res/probe3.yml'
                ]
            )
        )
