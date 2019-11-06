import datetime

from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

from src.datamigration.nwb_creator.pos_extractor import POSExtractor


class NWBFileCreator:

    def __init__(self,
                 experimenter_name='experimenter_name',
                 lab='lab',
                 institution='institution',
                 experiment_description='experiment_description',
                 session_description='session_description',
                 session_start_time=datetime.datetime.now(),
                 identifier='identifier',
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
        self.position = POSExtractor().getPosition()

    # def get_generated_task(self):
    #     self.task = task
    #     return self
    #
    # def get_electrode_locations(self):
    #     self.electrodes = electrodes
    #     return self
    #
    # def get_recording_device(self):
    #     self.recording_device = recording_device
    #     return self
    #
    # def get_generated_subject(self):
    #     self.subject = subject
    #     return self
    #
    # def get_generated_position(self):
    #     self.position = position
    #     return self

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

        with NWBHDF5IO('example_file_path.nwb', mode='w') as nwb_file:
            nwb_file.write(nwbfile)
