import datetime
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_builder.builders.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.builders.dio_builder import DioBuilder
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodesBuilder
from src.datamigration.nwb_builder.builders.electrode_group_builder import ElectrodeGroupBuilder
from src.datamigration.nwb_builder.builders.mda_builder import MdaBuilder
from src.datamigration.nwb_builder.builders.ntrodes_builder import NTrodesBuilder
from src.datamigration.nwb_builder.builders.position_builder import PositionBuilder
from src.datamigration.nwb_builder.builders.probe_builder import ProbesDictBuilder
from src.datamigration.nwb_builder.builders.task_builder import TaskBuilder
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.injectors.electrode_extension_injector import ElectrodeExtensionInjector
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.injectors.probe_injector import ProbeInjector
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_checker import HeaderChecker
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder

path = os.path.dirname(os.path.abspath(__file__))


class NWBFileBuilder:

    def __init__(self,
                 data_path,
                 animal_name,
                 date,
                 nwb_metadata,
                 process_dio=True,
                 process_mda=True,
                 output_file='output.nwb'
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

        self.__headers_validation()
        header = Header(self.data_path + '/' + self.animal_name + '/preprocessing/' +
                        self.date + '/header.xml')

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)
        self.position_builder = PositionBuilder(self.datasets)
        self.apparatus_builder = ApparatusBuilder(self.metadata['apparatus']['data'])

        self.ntrodes_builder = NTrodesBuilder(self.metadata)

        self.probes_builder = ProbesDictBuilder()
        self.probes_injector = ProbeInjector()

        self.electrode_group_builder = ElectrodeGroupBuilder()
        self.electrode_group_injector = ElectrodeGroupInjector()

        self.electrode_builder = ElectrodesBuilder()
        self.electrode_extension_injector = ElectrodeExtensionInjector()

        self.dio_builder = DioBuilder(self.datasets, self.metadata)
        self.mda_builder = MdaBuilder(self.metadata, header, self.datasets)



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

        self.__build_and_inject_processing_module(nwb_content)

        probes = self.__build_and_inject_probes(
            electrode_group_metadata=self.metadata['electrode groups'],
            probes_metadata=self.probes,
            nwb_content=nwb_content
        )

        electrode_groups = self.__build_and_inject_electrode_group(
            electrode_group_metadata=self.metadata['electrode groups'],
            nwb_content=nwb_content,
            probes=probes
        )

        self.__build_and_inject_electrodes(

        )

        self.ntrodes_builder.build(nwb_content)

        if self.process_dio:
            self.dio_builder.build(nwb_content)

        if self.process_mda:
            self.mda_builder.build(nwb_content)

        return nwb_content

    def write(self, content):
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()
        return self.output_file

    def __build_and_inject_processing_module(self, nwb_content):
        task = self.task_builder.build()
        position = self.position_builder.build()
        apparatus = self.apparatus_builder.build()

        self.pm_creator.insert(task)
        self.pm_creator.insert(position)
        self.pm_creator.insert(apparatus)

        nwb_content.add_processing_module(self.pm_creator.processing_module)

    def __build_and_inject_probes(self, electrode_group_metadata, probes_metadata, nwb_content):
        probes = self.probes_builder.build(electrode_group_metadata, probes_metadata)
        self.probes_injector.inject_all_probes(nwb_content, probes) #ToDo or dont pass nwb_content and make it here
        return probes

    def __build_and_inject_electrode_group(self, electrode_group_metadata, nwb_content, probes):
        electrode_groups = self.electrode_group_builder.build(electrode_group_metadata, probes)
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, electrode_groups)
        return electrode_groups

    def __build_and_inject_electrodes(self, electrode_group_metadata, nwb_content, probes):
        self.electrode_builder.build(electrode_group_metadata, probes)
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, electrode_groups)
        return electrode_groups

    def __headers_validation(self):
        rec_finder = RecFileFinder()
        header_checker = HeaderChecker(rec_finder.find_rec_files(path=(self.data_path
                                                                       + '/' + self.animal_name
                                                                       + '/raw/'
                                                                       + self.date)))
        header_checker.log_headers_compatibility()
