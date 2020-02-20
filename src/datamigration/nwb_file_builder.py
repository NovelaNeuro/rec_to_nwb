import datetime
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.header.module.header import Header
from src.datamigration.nwb.components.apparatus.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb.components.dio.dio_files import DioFiles
from src.datamigration.nwb.components.task.task_builder import TaskBuilder
from src.datamigration.nwb.components.dio.dio_builder import DioBuilder
from src.datamigration.nwb.components.dio.dio_injector import DioInjector
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder
from src.datamigration.nwb_builder.builders.electrode_extension_builder import ElectrodeExtensionBuilder
from src.datamigration.nwb_builder.builders.electrode_group_dict_builder import ElectrodeGroupDictBuilder
from src.datamigration.nwb_builder.builders.mda_builder import MdaBuilder
from src.datamigration.nwb_builder.builders.ntrodes_builder import NTrodesBuilder
from src.datamigration.nwb_builder.builders.position_builder import PositionBuilder
from src.datamigration.nwb_builder.builders.probes_dict_builder import ProbesDictBuilder
from src.datamigration.nwb_builder.creators.device_factory import DeviceFactory
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.extractors.continuous_time_extractor import ContinuousTimeExtractor
from src.datamigration.nwb_builder.injectors.electrode_extension_injector import ElectrodeExtensionInjector
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.injectors.header_device_injector import HeaderDeviceInjector
from src.datamigration.nwb_builder.injectors.probe_injector import ProbeInjector
from src.datamigration.nwb.components.dio.dio_manager import DioManager
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_processor import HeaderProcessor
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
        self.datasets = [self.data_folder.data[animal_name][date][dataset] for dataset in self.dataset_names]
        self.process_dio = process_dio
        self.process_mda = process_mda
        self.output_file = output_file
        self.metadata = nwb_metadata.metadata
        self.probes = nwb_metadata.probes

        rec_files_list = RecFileFinder().find_rec_files(

            path=(self.data_path
                  + '/' + self.animal_name
                  + '/raw/'
                  + self.date))

        header_file = HeaderProcessor.process_headers(rec_files_list)
        self.header = Header(header_file)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)
        self.position_builder = PositionBuilder(self.datasets)
        self.apparatus_builder = ApparatusBuilder(self.metadata['apparatus']['data'])

        self.ntrodes_builder = NTrodesBuilder(self.metadata)

        self.probes_dict_builder = ProbesDictBuilder(self.probes, self.metadata['electrode groups'])
        self.probes_injector = ProbeInjector()
        self.header_device_creator = DeviceFactory()
        self.header_device_injector = HeaderDeviceInjector()

        self.electrode_group_builder = ElectrodeGroupDictBuilder(self.metadata['electrode groups'])
        self.electrode_group_injector = ElectrodeGroupInjector()

        self.electrode_builder = ElectrodeBuilder(self.probes, self.metadata['electrode groups'])

        self.electrode_extension_builder = ElectrodeExtensionBuilder(self.probes, self.metadata['electrode groups'],
                                                                     self.header)
        self.electrode_extension_injector = ElectrodeExtensionInjector()

        # ToDo move lines below to another class
        continuous_time_files = [single_dataset.get_continuous_time() for single_dataset in self.datasets]
        self.continuous_time_dicts = ContinuousTimeExtractor.get_continuous_time_dict(continuous_time_files)
        self.dio_directories = [single_dataset.get_data_path_from_dataset('DIO') for single_dataset in self.datasets]

        self.mda_builder = MdaBuilder(self.metadata, self.header, self.datasets)

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

        probes_dict = self.__build_and_inject_probes(nwb_content)

        self.__build_and_inject_header_device(nwb_content, self.header)

        electrode_group_dict = self.__build_and_inject_electrode_group(nwb_content, probes_dict)

        self.__build_and_inject_electrodes(nwb_content, electrode_group_dict)

        self.__build_and_inject_electrodes_extensions(nwb_content)

        self.ntrodes_builder.build(nwb_content)

        if self.process_dio:
            self.__build_and_inject_dio(nwb_content)

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

    def __build_and_inject_header_device(self, nwb_content, header):
        header_device = self.header_device_creator.create_header_device(
            global_configuration=header.configuration.global_configuration,
            name='header_device')
        self.header_device_injector.inject_header_device(nwb_content, header_device)

    def __build_and_inject_probes(self, nwb_content):
        probes_dict = self.probes_dict_builder.build()
        self.probes_injector.inject_all_probes(nwb_content, probes_dict)
        return probes_dict

    def __build_and_inject_electrode_group(self, nwb_content, probes):
        electrode_group_dict = self.electrode_group_builder.build(probes)
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, electrode_group_dict)
        return electrode_group_dict

    def __build_and_inject_electrodes(self, nwb_content, electrode_group_dict):
        self.electrode_builder.build(nwb_content, electrode_group_dict)

    def __build_and_inject_electrodes_extensions(self, nwb_content):
        electrodes_metadata_extension, electrodes_header_extension = self.electrode_extension_builder.build()
        self.electrode_extension_injector.inject_extensions(
            nwb_content,
            electrodes_metadata_extension,
            electrodes_header_extension
        )

    def __build_and_inject_dio(self, nwb_content):
        dio_files = DioFiles(self.dio_directories, self.metadata['behavioral_events'])
        dio_manager = DioManager(dio_files=dio_files.get_files(),
                                 dio_metadata=self.metadata['behavioral_events'],
                                 continuous_time_dicts=self.continuous_time_dicts)
        dio_data = dio_manager.get_dio()
        dio_builder = DioBuilder(dio_data, self.metadata['behavioral_events'])
        dio_injector = DioInjector(nwb_content)
        dio_injector.inject(dio_builder.build(), 'behavior')
