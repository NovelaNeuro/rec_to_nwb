import datetime
import logging
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import src.datamigration.tools.file_scanner as fs
from src.datamigration.header.module.header import Header
from src.datamigration.nwb_components.apparatus.apparatus_builder import ApparatusBuilder
from src.datamigration.nwb_builder.builders.dio_builder import DioBuilder
from src.datamigration.nwb_builder.builders.electrode_builder import ElectrodeBuilder
from src.datamigration.nwb_builder.builders.electrode_extension_builder import ElectrodeExtensionBuilder
from src.datamigration.nwb_builder.builders.electrode_group_dict_builder import ElectrodeGroupDictBuilder
from src.datamigration.nwb_builder.builders.mda_builder import MdaBuilder
from src.datamigration.nwb_builder.builders.ntrodes_builder import NTrodesBuilder
from src.datamigration.nwb_builder.builders.position_builder import PositionBuilder
from src.datamigration.nwb_builder.builders.probes_dict_builder import ProbesDictBuilder
from src.datamigration.nwb_builder.builders.task_builder import TaskBuilder
from src.datamigration.nwb_builder.creators.header_device_creator import HeaderDeviceFactory
from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.injectors.electrode_extension_injector import ElectrodeExtensionInjector
from src.datamigration.nwb_builder.injectors.electrode_group_injector import ElectrodeGroupInjector
from src.datamigration.nwb_builder.injectors.header_device_injector import HeaderDeviceInjector
from src.datamigration.nwb_builder.injectors.probe_injector import ProbeInjector
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_comparator import HeaderComparator
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.header_extractor import HeaderFilesExtractor
from src.datamigration.nwb_builder.nwb_builder_tools.header_checker.rec_file_finder import RecFileFinder

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


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

        rec_finder = RecFileFinder()
        rec_files_list = rec_finder.find_rec_files(path=(self.data_path
                                                         + '/' + self.animal_name
                                                         + '/raw/'
                                                         + self.date))

        header_file = self.__headers_processing(rec_files_list)
        self.header = Header(header_file)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)
        self.position_builder = PositionBuilder(self.datasets)
        self.apparatus_builder = ApparatusBuilder(self.metadata['apparatus']['data'])

        self.ntrodes_builder = NTrodesBuilder(self.metadata)

        self.probes_dict_builder = ProbesDictBuilder(self.probes, self.metadata['electrode groups'])
        self.probes_injector = ProbeInjector()
        self.header_device_creator = HeaderDeviceFactory()
        self.header_device_injector = HeaderDeviceInjector()

        self.electrode_group_builder = ElectrodeGroupDictBuilder(self.metadata['electrode groups'])
        self.electrode_group_injector = ElectrodeGroupInjector()

        self.electrode_builder = ElectrodeBuilder(self.probes, self.metadata['electrode groups'])

        self.electrode_extension_builder = ElectrodeExtensionBuilder(self.probes, self.metadata['electrode groups'], self.header)
        self.electrode_extension_injector = ElectrodeExtensionInjector()

        self.dio_builder = DioBuilder(self.datasets, self.metadata)
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

    def __build_and_inject_header_device(self, nwb_content, header):
        header_device = self.header_device_creator.create(
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

    def __headers_processing(self, rec_files_list):

        headers_extractor = HeaderFilesExtractor()
        header_files = headers_extractor.extract_headers_from_rec_files(rec_files_list)
        header_comparator = HeaderComparator(header_files)
        headers_differences = header_comparator.compare()

        if headers_differences != []:
            message = 'Rec files: ' + str(rec_files_list) + ' contain incosistent xml headers!\n'
            differences = [diff for diff in headers_differences
                           if 'systemTimeAtCreation' not in str(diff) and 'timestampAtCreation'
                           not in str(diff)]
            logger.warning('%s , %s', message, differences)

        return header_files[0]
