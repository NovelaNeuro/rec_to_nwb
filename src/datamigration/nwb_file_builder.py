import datetime
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.builders.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.builders.electrode_structure_builder import ElectrodeStructureBuilder
from src.datamigration.nwb_builder.builders.ntrodes_builder import NTrodesBuilder
from src.datamigration.nwb_builder.builders.position_builder import PositionBuilder
from src.datamigration.nwb_builder.builders.processing_module_builder import ProcessingModuleBuilder
from src.datamigration.nwb_builder.builders.task_builder import TaskBuilder
from src.datamigration.nwb_builder.managers.processing_module_manager import ProcessingModuleManager
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

        self.task_builder = TaskBuilder(self.metadata)
        self.position_builder = PositionBuilder(self.datasets)
        self.apparatus_builder = ApparatusBuilder(self.metadata)
        self.ntrodes_builder = NTrodesBuilder(self.metadata)

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

        processing_module_builder = ProcessingModuleBuilder(nwb_content)
        processing_module = processing_module_builder.build('behavior', 'processing module for all behavior-related data')
        processing_module_manager = ProcessingModuleManager(processing_module)

        task = self.task_builder.build()
        processing_module_manager.add_data(task)

        position = self.position_builder.build()
        processing_module_manager.add_data(position)

        apparatus = self.apparatus_builder.build()
        processing_module_manager.add_data(apparatus)

        ElectrodeStructureBuilder().build_electrode_structure(
            metadata=self.metadata,
            header=self.header,
            nwb_content=nwb_content,
            probes=self.probes
        )

        self.ntrodes_builder.build(nwb_content)

        # # ToDo Waiting for WB
        # if self.process_dio:
        #     build_dio(self.metadata,
        #               self.data_path + '/' + self.animal_name + '/preprocessing/' + self.date,
        #               nwb_content)

        # if self.process_mda:
        #     build_mda(self.header,
        #               self.metadata,
        #               self.datasets,
        #               nwb_content)

        return nwb_content

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file
