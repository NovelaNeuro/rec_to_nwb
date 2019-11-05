import os

import numpy as np
from mountainlab_pytools.mdaio import readmda
from pynwb import NWBFile, NWBHDF5IO, ecephys
from pynwb import ProcessingModule
from pynwb.behavior import Position, SpatialSeries
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject

from experiment_data import ExperimentData


class NWBFileCreator:

    def __init__(self,
                 experimenter_name,
                 lab,
                 institution,
                 experiment_description,
                 session_description,
                 session_start_time,
                 identifier,
                 ):

        self.experimenter_name = experimenter_name
        self.lab = lab
        self.institution = institution
        self.experiment_description = experiment_description
        self.session_description = session_description
        self.session_start_time = session_start_time
        self.identifier = identifier
        self.task = None
        self.electrode_locations = None
        self.recording_device = None
        self.subject = None
        self.electrodes = None
        self.position = None

    def with_task(self, name, description, id=None, columns=None, colnames=None,
                  start_time=None, stop_time=None, tags=None, timeseries=None):
        self.task = TimeIntervals(name, description, id, columns, colnames)
        if not (start_time is None or stop_time is None):
            self.task.add_interval(start_time, stop_time, tags, timeseries)
        return self

    def with_generated_task(self, task):
        self.task = task
        return self

    def with_electrode_locations(self, electrodes):
        self.electrodes = electrodes
        return self

    def with_recording_device(self, recording_device):
        self.recording_device = recording_device
        return self

    def with_subject(self, age, description, genotype, sex, species, subject_id, weight, date_of_borth):
        self.subject = Subject(age, description, genotype, sex, species, subject_id, weight, date_of_borth)
        return self

    def with_generated_subject(self, subject):
        self.subject = subject
        return self

    def with_position(self, name, data, reference_frame, timestamps):
        spatial_series = SpatialSeries(name=name,
                                       data=data,
                                       reference_frame=reference_frame,
                                       timestamps=timestamps,
                                       )
        self.position = Position(spatial_series=spatial_series)
        return self

    def with_generated_position(self, position):
        self.position = position
        return self

    def build(self):
        nwbfile = NWBFile(session_description=self.session_description,
                          experimenter=self.experimenter_name,
                          lab=self.lab,
                          institution=self.institution,
                          session_start_time=self.session_start_time,
                          identifier=self.identifier,
                          experiment_description=self.experiment_description,
                          subject=self.subject,
                          )

        if (self.task):
            task_module = ProcessingModule(name='task',
                                           description='testDescription')
            nwbfile.add_processing_module(task_module).add(self.task)

        if (self.position):
            position_module = ProcessingModule(name='position',
                                               description='testDescription')
            nwbfile.add_processing_module(position_module).add(self.position)

        device = nwbfile.create_device(name='name_test22')
        electrode_name = 'electrode_name_test22'
        description = "description_test22"
        location = "location_test22"
        electrode_group = nwbfile.create_electrode_group(electrode_name,
                                                         description=description,
                                                         location=location,
                                                         device=device)
        for idx in [1, 2, 3, 4]:
            nwbfile.add_electrode(idx,
                                  x=1.0, y=2.0, z=3.0,
                                  imp=float(-idx),
                                  location='CA1', filtering='none',
                                  group=electrode_group)
        electrode_table_region = nwbfile.create_electrode_table_region([0, 2], 'the first and third electrodes')
        rate = 10.0
        np.random.seed(1234)
        data_len = 1000
        ephys_data = np.random.rand(data_len * 2)
        ephys_timestamps = np.arange(data_len) / rate
        electrode_location = ecephys.ElectricalSeries('electrode_location_test',
                                                      ephys_data,
                                                      electrode_table_region,
                                                      timestamps=ephys_timestamps,
                                                      resolution=0.001,
                                                      comments="This data was randomly generated with numpy, using 1234 as the seed",
                                                      description="Random numbers generated with numpy.random.rand")
        nwbfile.add_acquisition(electrode_location)

        for idx in range(64):
            nwbfile.add_electrode(idx,
                                  x=1.0, y=2.0, z=3.0,
                                  imp=float(-idx),
                                  location='CA1', filtering='none',
                                  group=electrode_group)

        timestamps = readmda(ExperimentData.mda_path + ExperimentData.mda_timestamp)

        mda_files = [mda_file for mda_file in os.listdir(ExperimentData.mda_path) if
                     (mda_file.endswith('.mda') and mda_file != ExperimentData.mda_timestamp)]

        counter = 0
        for file in mda_files:
            electrode_table_region = nwbfile.create_electrode_table_region([counter % 4], "description")
            name = "test" + str(counter)
            series = ecephys.ElectricalSeries(name,
                                              readmda(ExperimentData.mda_path + ExperimentData.mda_file)[counter % 4],
                                              electrode_table_region,
                                              timestamps=timestamps,
                                              # Alternatively, could specify starting_time and rate as follows
                                              # starting_time=ephys_timestamps[0],
                                              # rate=rate,
                                              resolution=0.001,
                                              comments="aaa",
                                              description="Electrical series registered on electrode " + str(counter))
            nwbfile.add_acquisition(series)
            counter = counter + 1

        with NWBHDF5IO('example_file_path.nwb', mode='w') as nwb_file:
            nwb_file.write(nwbfile)

