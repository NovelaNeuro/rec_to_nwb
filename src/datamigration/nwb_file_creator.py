from pynwb import NWBHDF5IO, NWBFile
from pynwb.epoch import TimeIntervals
from pynwb.file import Subject


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

    def with_task(self, name, description, id=None, columns=None, colnames=None,
                  start_time=None, stop_time=None, tags=None, timeseries=None):
        self.task = TimeIntervals(name, description, id, columns, colnames)
        if not (start_time is None or stop_time is None):
            self.task.add_interval(start_time, stop_time, tags, timeseries)
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

    def build(self):
        nwbfile = NWBFile(session_description=self.session_description,
                          experimenter=self.experimenter_name,
                          lab=self.lab,
                          institution=self.institution,
                          session_start_time=self.session_start_time,
                          identifier=self.identifier,
                          experiment_description=self.experiment_description,
                          subject=self.subject,
                          task=self.task,
                          )

        with NWBHDF5IO('example_file_path.nwb', mode='w') as nwb_file:
            nwb_file.write(nwbfile)