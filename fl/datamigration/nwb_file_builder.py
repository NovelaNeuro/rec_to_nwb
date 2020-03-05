import datetime
import logging.config
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

import fl.datamigration.tools.file_scanner as fs
from fl.datamigration.header.header_checker.header_processor import HeaderProcessor
from fl.datamigration.header.header_checker.rec_file_finder import RecFileFinder
from fl.datamigration.header.module.header import Header
from fl.datamigration.nwb.components.apparatus.apparatus_creator import ApparatusCreator
from fl.datamigration.nwb.components.apparatus.fl_apparatus_manager import FlApparatusManager
from fl.datamigration.nwb.components.device.device_factory import DeviceFactory
from fl.datamigration.nwb.components.device.device_injector import DeviceInjector
from fl.datamigration.nwb.components.device.fl_device_header_manager import FlDeviceHeaderManager
from fl.datamigration.nwb.components.device.fl_probe_manager import FlProbeManager
from fl.datamigration.nwb.components.dio.dio_builder import DioBuilder
from fl.datamigration.nwb.components.dio.dio_files import DioFiles
from fl.datamigration.nwb.components.dio.dio_injector import DioInjector
from fl.datamigration.nwb.components.dio.dio_manager import DioManager
from fl.datamigration.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_creator import FlElectrodeGroupCreator
from fl.datamigration.nwb.components.electrode_group.fl_electrode_group_manager import FlElectrodeGroupManager
from fl.datamigration.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from fl.datamigration.nwb.components.electrodes.electrode_extension_creator import ElectrodeExtensionCreator
from fl.datamigration.nwb.components.electrodes.electrode_extension_injector import ElectrodeExtensionInjector
from fl.datamigration.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager
from fl.datamigration.nwb.components.mda.electrical_series_creator import ElectricalSeriesCreator
from fl.datamigration.nwb.components.mda.fl_mda_manager import FlMdaManager
from fl.datamigration.nwb.components.mda.mda_injector import MdaInjector
from fl.datamigration.nwb.components.position.fl_position_manager import FlPositionManager
from fl.datamigration.nwb.components.position.position_creator import PositionCreator
from fl.datamigration.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator
from fl.datamigration.nwb.components.task.task_builder import TaskBuilder

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NWBFileBuilder:
    """unpack data from preprocessing folder specified by arguments, and write those data into NWB file format"""

    def __init__(self,
                 data_path,
                 animal_name,
                 date,
                 nwb_metadata,
                 rec_config,
                 process_dio=True,
                 process_mda=True,
                 output_file='output.nwb'
                 ):

        logger.info('NWBFileBuilder initialization')

        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.data_scanner = fs.DataScanner(data_path, animal_name)
        self.dataset_names = self.data_scanner.get_all_datasets(animal_name, date)
        self.datasets = [self.data_scanner.data[animal_name][date][dataset] for dataset in self.dataset_names]
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
        if rec_config is not None:
            header_file = rec_config
        else:
            header_file = HeaderProcessor.process_headers(rec_files_list)
        self.header = Header(header_file)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)

        self.fl_position_manager = FlPositionManager(self.datasets)
        self.position_creator = PositionCreator()

        self.fl_apparatus_manager = FlApparatusManager(self.metadata['apparatus']['data'])

        self.fl_probe_manager = FlProbeManager(self.probes, self.metadata['electrode groups'])
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

        self.fl_device_header_manager = FlDeviceHeaderManager('header_device',
                                                              self.header.configuration.global_configuration)


        self.fl_electrode_group_manager = FlElectrodeGroupManager(self.metadata['electrode groups'])
        self.fl_electrode_group_creator = FlElectrodeGroupCreator()
        self.electrode_group_injector = ElectrodeGroupInjector()

        self.fl_electrode_manager = FlElectrodeManager(self.probes, self.metadata['electrode groups'])
        self.electrode_creator = ElectrodesCreator()

        self.electrode_extension_creator = ElectrodeExtensionCreator(
            self.probes,
            self.metadata['electrode groups'],
            self.metadata['ntrode probe channel map'],
            self.header
        )
        self.electrode_extension_injector = ElectrodeExtensionInjector()

    def build(self):
        logger.info('Building components for NWB')

        nwb_content = NWBFile(
            session_description=self.metadata['session description'],
            experimenter=self.metadata['experimenter name'],
            lab=self.metadata['lab'],
            institution=self.metadata['institution'],
            session_start_time=datetime.datetime.strptime(self.metadata['session start time'], '%m/%d/%Y %H:%M:%S'),
            identifier=str(uuid.uuid1()),
            experiment_description=self.metadata['experiment description'],
            subject=Subject(
                description=self.metadata['subject']['description'],
                genotype=self.metadata['subject']['genotype'],
                sex=self.metadata['subject']['sex'],
                species=self.metadata['subject']['species'],
                subject_id=self.metadata['subject']['subject id'],
                weight=str(self.metadata['subject']['weight']
                           ),
            ),
        )

        self.__build_and_inject_processing_module(nwb_content)

        probes = self.__build_and_inject_probes(nwb_content)

        self.__build_and_inject_header_device(nwb_content)

        fl_electrode_groups = self.__build_and_inject_fl_electrode_group(nwb_content, probes)

        self.__build_and_inject_electrodes(nwb_content, fl_electrode_groups)

        self.__build_and_inject_electrodes_extensions(nwb_content)

        if self.process_dio:
            self.__build_and_inject_dio(nwb_content)

        if self.process_mda:
            self.__build_and_inject_mda(nwb_content)

        return nwb_content

    def write(self, content):
        """write nwb file handler with colected data into actual file"""

        logger.info('Writing down content to ' + self.output_file)
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()

        logger.info(self.output_file + ' file has been created.')
        return self.output_file

    def __build_and_inject_processing_module(self, nwb_content):
        logger.info('Apparatus: Building')
        fl_apparatus = self.fl_apparatus_manager.get_fl_apparatus()
        logger.info('Apparatus: Creating')
        apparatus = ApparatusCreator.create_apparatus(fl_apparatus)
        logger.info('Apparatus: Injecting into ProcessingModule')
        self.pm_creator.insert(apparatus)

        logger.info('Task: Building')
        task = self.task_builder.build()
        logger.info('Task: Injecting into ProcessingModule')
        self.pm_creator.insert(task)

        logger.info('Position: Building')
        fl_position = self.fl_position_manager.get_fl_position()
        logger.info('Position: Creating')
        position = self.position_creator.create(fl_position)
        logger.info('Position: Injecting into ProcessingModule')
        self.pm_creator.insert(position)

        nwb_content.add_processing_module(self.pm_creator.processing_module)

    def __build_and_inject_header_device(self, nwb_content):
        logger.info('HeaderDevice: Building')
        fl_header_device = self.fl_device_header_manager.get_fl_header_device()
        logger.info('HeaderDevice: Creating')
        header_device = self.device_factory.create_header_device(fl_header_device)
        logger.info('HeaderDevice: Injecting into NWB')
        self.device_injector.inject_all_devices(nwb_content, [header_device])

    def __build_and_inject_probes(self, nwb_content):
        logger.info('Probes: Building')
        fl_probe_list = self.fl_probe_manager.get_fl_probes_list()
        logger.info('Probes: Creating probes')
        probes = [self.device_factory.create_probe(fl_probe) for fl_probe in fl_probe_list]
        logger.info('Probes: Injecting probes into NWB')
        self.device_injector.inject_all_devices(nwb_content, probes)
        return probes

    def __build_and_inject_fl_electrode_group(self, nwb_content, probes):
        logger.info('ElectrodeGroups: Building')
        fl_fl_electrode_groups = self.fl_electrode_group_manager.get_fl_fl_electrode_groups(probes)
        logger.info('ElectrodeGroups: Creating')
        fl_electrode_groups = [self.fl_electrode_group_creator.create(fl_electrode_group)
                            for fl_electrode_group in fl_fl_electrode_groups]
        logger.info('ElectrodeGroups: Injecting into NWB')
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, fl_electrode_groups)
        return fl_electrode_groups

    def __build_and_inject_electrodes(self, nwb_content, electrode_groups):
        logger.info('Electrodes: Building')
        fl_electrodes = self.fl_electrode_manager.get_fl_electrodes(electrode_groups)
        logger.info('Electrodes: Creating&Injecting into NWB')
        [self.electrode_creator.create(nwb_content, fl_electrode) for fl_electrode in fl_electrodes]

    def __build_and_inject_electrodes_extensions(self, nwb_content):
        logger.info('ElectrodesExtensions: Building')
        electrodes_metadata_extension, electrodes_header_extension, electrodes_ntrodes_extension = \
            self.electrode_extension_creator.create()

        logger.info('ElectrodesExtensions: Injecting into NWB')
        self.electrode_extension_injector.inject_extensions(
            nwb_content,
            electrodes_metadata_extension,
            electrodes_header_extension,
            electrodes_ntrodes_extension
        )

    def __build_and_inject_dio(self, nwb_content):
        logger.info('DIO: Prepare directories')
        dio_directories = [single_dataset.get_data_path_from_dataset('DIO') for single_dataset in self.datasets]

        logger.info('DIO: Prepare files')
        dio_files = DioFiles(dio_directories, self.metadata['behavioral_events'])

        dio_manager = DioManager(dio_files=dio_files.get_files(),
                                 dio_metadata=self.metadata['behavioral_events'],
                                 continuous_time_files=self.__get_continuous_time_files())
        logger.info('DIO: Retrieve data')
        dio_data = dio_manager.get_dio()

        dio_builder = DioBuilder(dio_data, self.metadata['behavioral_events'])
        dio_injector = DioInjector(nwb_content)

        logger.info('DIO: Building&Injecting into NWB')
        dio_injector.inject(dio_builder.build(), 'behavior')

    def __get_continuous_time_files(self):
        return [single_dataset.get_continuous_time() for single_dataset in self.datasets]

    def __build_and_inject_mda(self, nwb_content):
        logger.info('MDA: Building')

        fl_mda_manager = FlMdaManager(
            nwb_content,
            self.metadata,
            self.header.configuration.hardware_configuration.sampling_rate,
            self.datasets
        )
        MdaInjector.inject_mda(nwb_content=nwb_content,
                               electrical_series=ElectricalSeriesCreator.create_mda(fl_mda_manager.get_data()))
