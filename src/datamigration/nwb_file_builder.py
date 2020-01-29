import datetime
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.builders.apparatus_builder import build_apparatus
from src.datamigration.nwb_builder.builders.dio_builder import build_dio
from src.datamigration.nwb_builder.builders.electrode_structure_builder import ElectrodeStructureBuilder
from src.datamigration.nwb_builder.builders.mda_builder import build_mda
from src.datamigration.nwb_builder.builders.ntrodes_builder import build_ntrodes
from src.datamigration.nwb_builder.builders.pos_builder import build_position
from src.datamigration.nwb_builder.builders.task_builder import build_task
from src.datamigration.nwb_builder.injectors.processing_module_injector import build_processing_module
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_checker import check_headers_compatibility

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self,
                 data_path,
                 animal_name,
                 date,
                 nwb_metadata,
                 output_file='output.nwb',
                 process_dio=True,
                 process_mda=True
                 ):

        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_folder = fs.DataScanner(data_path)
        self.dataset_names = self.data_folder.get_all_datasets(animal_name, date)
        self.datasets = [self.data_folder.data[animal_name][date][dataset_mda] for dataset_mda in self.dataset_names]
        self.process_dio = process_dio
        self.process_mda = process_mda
        self.output_file = output_file
        self.metadata = nwb_metadata.metadata
        self.probes = nwb_metadata.probes

        check_headers_compatibility(self.data_path, self.animal_name, self.date)

        self.header = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                             self.date + '/header.xml')
        self.spike_n_trodes = self.header.configuration.spike_configuration.spike_n_trodes

    def build(self):
        nwb_content = NWBFile(session_description=self.metadata['session description'],
                              experimenter=self.metadata['experimenter name'],
                              lab=self.metadata['lab'],
                              institution=self.metadata['institution'],
                              session_start_time=datetime.datetime.strptime(
                                                  self.metadata['session start time'], '%m/%d/%Y %H:%M:%S'),
                              identifier=str(uuid.uuid1()),
                              experiment_description=self.metadata['experiment description'],
                              subject=Subject(
                                              description=self.metadata['subject']['description'],
                                              genotype=self.metadata['subject']['genotype'],
                                              sex=self.metadata['subject']['sex'],
                                              species=self.metadata['subject']['species'],
                                              subject_id=self.metadata['subject']['subject id'],
                                              weight=str(self.metadata['subject']['weight']),
                                             ),
                              )
        build_processing_module('behavior', 'processing module for all behavior-related data', nwb_content)

        build_task(self.metadata, nwb_content)

        build_position(self.datasets, nwb_content)

        build_apparatus(self.metadata, nwb_content)

        ElectrodeStructureBuilder().build_electrode_structure(metadata=self.metadata,
                                  header=self.header,
                                  nwb_content=nwb_content,
                                  probes=self.probes)

        build_ntrodes(self.metadata, nwb_content)

        if self.process_dio:
            build_dio(self.metadata,
                      self.data_path + '/' + self.animal_name + '/preprocessing/' + self.date,
                      nwb_content)

        if self.process_mda:
            build_mda(self.header,
                      self.metadata,
                      self.datasets,
                      nwb_content)

        return nwb_content

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
