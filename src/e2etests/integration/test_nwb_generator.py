import datetime
import os
import unittest

import pandas as pd
import pynwb
from pynwb import NWBHDF5IO
from pynwb.behavior import Position
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from src.datamigration.nwb_file_creator import NWBFileCreator
from src.e2etests.integration.experiment_data import ExperimentData


class NWBGenerator(unittest.TestCase):

    def setUp(self):
        position = self.getPosition()
        subject = self.getSubject()
        task = self.getTask()

        NWBFileCreator(
            'name_test',
            'lab_test',
            'institution_test',
            'experiment_description_test',
            'session_description_test',
            datetime.datetime.now(),
            'identifier',
        ) \
            .with_generated_task(task) \
            .with_generated_subject(subject) \
            .with_generated_position(position) \
            .build()

    def getTask(self):
        task = TimeIntervals("name_test", description="description_test", id=None, columns=None, colnames=None)
        task.add_interval(1.0, 10.0, tags=None, timeseries=None)
        return task

    def getSubject(self):
        subject = Subject('age_test', 'description_test', 'genotype_test', 'sex_test', 'species_test',
                          'subject_id_test', 'weight_test', datetime.datetime.now())
        return subject

    def getPosition(self):
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file
        self.pos_online = readTrodesExtractedDataFile(self.path_to_beans)
        position_online = pd.DataFrame(self.pos_online['data'])
        position = Position()
        position.create_spatial_series(
            name="TestName",
            data=(position_online.xloc, position_online.yloc, position_online.xloc2, position_online.yloc2),
            # What should be inside this field?
            reference_frame="Description defining what the zero-position is",
            timestamps=position_online.time.tolist()
        )
        return position

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
