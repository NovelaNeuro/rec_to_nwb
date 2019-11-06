import datetime
import os
import unittest

import pandas as pd
import pynwb
from pynwb import NWBHDF5IO
from pynwb.behavior import Position, SpatialSeries
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject
from rec_to_binaries.read_binaries import readTrodesExtractedDataFile

from experiment_data import ExperimentData
from src.datamigration.nwb_file_creator import NWBFileCreator


class NWBGenerator(unittest.TestCase):

    def setUp(self):
        position = self.getPosition()
        subject = getSubject()
        task = getTask()

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

    def getPosition(self):
        self.path_to_beans = ExperimentData.pos_path + ExperimentData.pos_file
        self.pos_online = readTrodesExtractedDataFile(self.path_to_beans)
        position_online = pd.DataFrame(self.pos_online['data'])
        series = SpatialSeries(
            name="TestName",
            data=(position_online.xloc, position_online.yloc, position_online.xloc2, position_online.yloc2),
            # What should be inside this field?
            reference_frame="Description defining what the zero-position is",
            timestamps=position_online.time.tolist()
        )
        position = Position(spatial_series=series)
        return position

    def test_file_exist(self):
        self.assertNotEqual(0, os.path.getsize('example_file_path.nwb'))

    def test_task(self):
        with NWBHDF5IO(path='example_file_path.nwb', mode='a') as io:
            nwbfile = io.read()
            self.assertEqual(
                isinstance(nwbfile.processing['task'].data_interfaces['name_test'], pynwb.epoch.TimeIntervals),
                True,
                'Type of this object should be pynwb.epoch.TimeIntervals'
            )

    def test_subject(self):
        with NWBHDF5IO(path='example_file_path.nwb', mode='a') as io:
            nwbfile = io.read()
            self.assertEqual(
                isinstance(nwbfile.subject, pynwb.file.Subject),
                True,
                'Type of this object should be pynwb.file.Subject'
            )

    def test_position(self):
        with NWBHDF5IO(path='example_file_path.nwb', mode='a') as io:
            nwbfile = io.read()
            self.assertEqual(
                isinstance(nwbfile.processing['position'].data_interfaces['Position'], pynwb.behavior.Position),
                True,
                'Type of this object should be pynwb.behavior.Position'
            )


def getTask():
    task = TimeIntervals(name="name_test", description="description_test", id=None, columns=None, colnames=None)
    task.add_interval(start_time=1.0, stop_time=10.0, tags=None, timeseries=None)
    return task


def getSubject():
    subject = Subject('age_test', 'description_test', 'genotype_test', 'sex_test', 'species_test',
                      'subject_id_test', 'weight_test', datetime.datetime.now())
    return subject
