from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime


class MetaDataToNWBFile:

    def __init__(self,
                 experimenter_name,
                 lab,
                 institution,
                 experiment_description,
                 session_description,
                 session_start_time,
                 identifier,
                 task
                 ):

        self.experimenter_name = experimenter_name
        self.lab = lab
        self.institution = institution
        self.experiment_description = experiment_description
        self.session_description = session_description
        self.session_start_time = session_start_time
        self.identifier = identifier
        self.task = task


new_metadata = MetaDataToNWBFile(experimenter_name='WojciechMerynda',
                                 lab='NovelaLab',
                                 institution='NovelaNeurotechnologies',
                                 experiment_description='experiment on monkeys',
                                 session_description='we studies monkeys',
                                 session_start_time=datetime(2019, 7, 10),
                                 identifier='magicidentifier',
                                 task='semenicetask'
                                 )

nwbfile = NWBFile(session_description=new_metadata.session_description,
                  experimenter=new_metadata.experimenter_name,
                  lab=new_metadata.lab,
                  institution=new_metadata.institution,
                  session_start_time=new_metadata.session_start_time,
                  identifier=new_metadata.identifier,
                  experiment_description=new_metadata.experiment_description,
                  intervals=[]
                  )

io = NWBHDF5IO('example_file_path.nwb', mode='w')
io.write(nwbfile)
io.close()

io = NWBHDF5IO('example_file_path.nwb', 'r')
nwbfile_in = io.read()

print(nwbfile_in)
