from pynwb import NWBHDF5IO, NWBFile
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

    def with_task(self, task):
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

        with NWBHDF5IO('example_file_path.nwb', mode='w') as nwb_file:
            nwb_file.write(nwbfile)


