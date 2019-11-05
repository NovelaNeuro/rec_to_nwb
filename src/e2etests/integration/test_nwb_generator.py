import datetime
import os
import unittest

import pynwb
from pynwb import NWBHDF5IO

from src.datamigration.nwb_file_creator import NWBFileCreator


class NWBGenerator(unittest.TestCase):

    def setUp(self):
        datetime_object = datetime.datetime.now()
        data = (1, 2, 3)
        timestamps = list(range(10))

        nwb_object = NWBFileCreator(
            'name_test',
            'lab_test',
            'institution_test',
            'experiment_description_test',
            'session_description_test',
            datetime_object,
            'identifier',
        ).with_task(
            'name_test',
            'description_test',
            id=None,
            columns=None,
            colnames=None,
            start_time=1.0,
            stop_time=2.0
        ).with_subject(
            'age_test',
            'description_test',
            'genotype_test',
            'sex_test',
            'species_test',
            'subject_id_test',
            'weight_test',
            datetime_object,
        ).with_position(
            'name_test',
            data,
            'reference_frame_test',
            timestamps
        ).build()

    def test_file_exist(self):
        self.assertNotEqual(0, os.path.getsize('example_file_path.nwb'))

    def test_task(self):
        io = NWBHDF5IO('example_file_path.nwb', mode='a')
        nwbfile = io.read()
        self.assertEqual(
            isinstance(nwbfile.processing['task'].data_interfaces['name_test'], pynwb.epoch.TimeIntervals),
            True,
            'Type of this object should be pynwb.epoch.TimeIntervals'
        )
        io.close()

    def test_subject(self):
        io = NWBHDF5IO('example_file_path.nwb', mode='a')
        nwbfile = io.read()
        self.assertEqual(
            isinstance(nwbfile.subject, pynwb.file.Subject),
            True,
            'Type of this object should be pynwb.file.Subject'
        )
        io.close()

    def test_position(self):
        io = NWBHDF5IO('example_file_path.nwb', mode='a')
        nwbfile = io.read()
        self.assertEqual(
            isinstance(nwbfile.processing['position'].data_interfaces['Position'], pynwb.behavior.Position),
            True,
            'Type of this object should be pynwb.behavior.Position'
        )
        io.close()
