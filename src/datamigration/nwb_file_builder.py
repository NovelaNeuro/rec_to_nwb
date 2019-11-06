from pynwb import NWBHDF5IO, NWBFile, ProcessingModule

from src.datamigration.nwb_creator.metadata_extractor import MetadataExtractor
from src.datamigration.nwb_creator.pos_extractor import POSExtractor


class NWBFileCreator:

    def __init__(self):
        metadate_extractor = MetadataExtractor()

        self.experimenter_name = metadate_extractor.experimenter_name
        self.lab = metadate_extractor.lab
        self.institution = metadate_extractor.institution
        self.experiment_description = metadate_extractor.experiment_description
        self.session_description = metadate_extractor.session_description
        self.session_start_time = metadate_extractor.session_start_time
        self.identifier = metadate_extractor.identifier
        self.task = metadate_extractor.task
        self.subject = metadate_extractor.subject
        self.position = POSExtractor().get_position()
        self.electrode_locations = None
        self.recording_device = None
        self.electrodes = None

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
