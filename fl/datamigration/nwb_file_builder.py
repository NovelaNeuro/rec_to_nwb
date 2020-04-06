import logging.config
import os
import uuid

from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

from fl.datamigration.exceptions.different_number_of_tasks_and_epochs_exception import \
    DifferentNumberOfTasksAndEpochsException
from fl.datamigration.header.header_checker.header_processor import HeaderProcessor
from fl.datamigration.header.header_checker.rec_file_finder import RecFileFinder
from fl.datamigration.header.module.header import Header
from fl.datamigration.metadata.metadata_manager import MetadataManager
from fl.datamigration.nwb.common.session_time_extractor import SessionTimeExtractor
from fl.datamigration.nwb.components.analog.analog_creator import AnalogCreator
from fl.datamigration.nwb.components.analog.analog_files import AnalogFiles
from fl.datamigration.nwb.components.analog.analog_injector import AnalogInjector
from fl.datamigration.nwb.components.analog.fl_analog_manager import FlAnalogManager
from fl.datamigration.nwb.components.device.device_factory import DeviceFactory
from fl.datamigration.nwb.components.device.device_injector import DeviceInjector
from fl.datamigration.nwb.components.device.fl_device_header_manager import FlDeviceHeaderManager
from fl.datamigration.nwb.components.device.fl_probe_manager import FlProbeManager
from fl.datamigration.nwb.components.dio.dio_builder import DioBuilder
from fl.datamigration.nwb.components.dio.dio_files import DioFiles
from fl.datamigration.nwb.components.dio.dio_injector import DioInjector
from fl.datamigration.nwb.components.dio.dio_manager import DioManager
from fl.datamigration.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from fl.datamigration.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector
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
from fl.datamigration.tools.data_scanner import DataScanner
from fl.datamigration.validation.not_empty_validator import NotEmptyValidator
from fl.datamigration.validation.task_validator import TaskValidator
from fl.datamigration.validation.metadata_validator import MetadataValidator
from fl.datamigration.validation.ntrode_validator import NTrodeValidator
from fl.datamigration.nwb.components.epochs.fl_epochs_manager import FlEpochsManager
from fl.datamigration.nwb.components.epochs.epochs_injector import EpochsInjector
from fl.datamigration.validation.preprocessing_validator import PreprocessingValidator
from fl.datamigration.validation.type_validator import TypeValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator

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
                 process_dio=True,
                 process_mda=True,
                 process_analog=True,
                 output_file='output.nwb'
                 ):

        """
        Args:
        data_path (string): path to directory containing all experiments data
        animal_name (string): directory name which represents animal subject of experiment
        date (string): date of experiment
        nwb_metadata (MetadataManager): object contains metadata about experiment
        process_dio (boolean): flag if dio data should be processed
        process_mda (boolean): flag if mda data should be processed
        process_analog (boolean): flag if analog data should be processed
        output_file (string): path and name specifying where .nwb file gonna be written
        """

        validation_registrator = ValidationRegistrator()
        validation_registrator.register(TypeValidator(data_path, str))
        validation_registrator.register(NotEmptyValidator(data_path))
        validation_registrator.register(TypeValidator(animal_name, str))
        validation_registrator.register(NotEmptyValidator(animal_name))
        validation_registrator.register(TypeValidator(date, str))
        validation_registrator.register(NotEmptyValidator(date))
        validation_registrator.register(TypeValidator(nwb_metadata, MetadataManager))
        validation_registrator.register(TypeValidator(output_file, str))
        validation_registrator.register(TypeValidator(process_analog, bool))
        validation_registrator.register(TypeValidator(process_dio, bool))
        validation_registrator.register(TypeValidator(process_mda, bool))
        validation_registrator.validate()

        logger.info('NWBFileBuilder initialization')
        logger.info(
            'NWB builder initialization parameters: \n'
            + 'data_path = ' + str(data_path) + '\n'
            + 'animal_name = ' + str(animal_name)  + '\n'
            + 'date = ' + str(date) + '\n'
            + 'nwb_metadata = ' + str(nwb_metadata) + '\n'
            + 'process_dio = ' + str(process_dio) + '\n'
            + 'process_mda = ' + str(process_mda) + '\n'
            + 'process_analog = ' + str(process_analog) + '\n'
            + 'output_file = ' + str(output_file) + '\n'
        )

        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.metadata = nwb_metadata.metadata
        self.probes = nwb_metadata.probes
        self.process_dio = process_dio
        self.process_mda = process_mda
        self.process_analog = process_analog
        self.output_file = output_file

        data_types_for_scanning = {'pos': True,
                                   'time': True,
                                   'mda': process_mda,
                                   'DIO': process_dio,
                                   'analog': process_dio}

        rec_files_list = RecFileFinder().find_rec_files(

            path=(self.data_path
                  + '/' + self.animal_name
                  + '/raw/'
                  + self.date))
        header_file = HeaderProcessor.process_headers(rec_files_list)
        self.header = Header(header_file)
        self.data_scanner = DataScanner(data_path, animal_name, nwb_metadata)
        self.dataset_names = self.data_scanner.get_all_epochs(date)
        full_data_path = data_path + '/' + animal_name + '/preprocessing/' + date

        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(NTrodeValidator(self.metadata, self.header))
        validationRegistrator.register(PreprocessingValidator(full_data_path,
                                                              self.dataset_names,
                                                              data_types_for_scanning))
        validationRegistrator.register(TaskValidator(len(self.dataset_names), self.metadata['tasks']))
        validationRegistrator.validate()

        self.extract_datasets(animal_name, date)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)

        self.fl_position_manager = FlPositionManager(self.datasets)
        self.position_creator = PositionCreator()

        self.fl_probe_manager = FlProbeManager(self.probes, self.metadata['electrode groups'])
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

        self.fl_device_header_manager = FlDeviceHeaderManager('header_device',
                                                              self.header.configuration.global_configuration)

        self.fl_electrode_group_manager = FlElectrodeGroupManager(self.metadata['electrode groups'])
        self.nwb_electrode_group_creator = ElectrodeGroupFactory()
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

        self.session_time_extractor = SessionTimeExtractor(
            self.datasets,
            self.animal_name,
            self.date,
            self.dataset_names
        )

    def extract_datasets(self, animal_name, date):
        self.data_scanner.extract_data_from_date_folder(date)
        self.datasets = [self.data_scanner.data[animal_name][date][dataset] for dataset in self.dataset_names]

    def build(self):
        logger.info('Building components for NWB')

        nwb_content = NWBFile(
            session_description=self.metadata['session description'],
            experimenter=self.metadata['experimenter name'],
            lab=self.metadata['lab'],
            institution=self.metadata['institution'],
            session_start_time=self.session_time_extractor.get_session_start_time(),
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

        nwb_electrode_groups = self.__build_and_inject_nwb_electrode_group(nwb_content, probes)

        self.__build_and_inject_electrodes(nwb_content, nwb_electrode_groups)

        self.__build_and_inject_electrodes_extensions(nwb_content)

        self.__build_and_inject_epochs(nwb_content)

        if self.process_dio:
            self.__build_and_inject_dio(nwb_content)

        if self.process_mda:
            self.__build_and_inject_mda(nwb_content)

        if self.process_analog:
            self.__build_and_inject_analog(nwb_content)

        return nwb_content

    def write(self, content):
        """write nwb file handler with colected data into actual file"""

        logger.info('Writing down content to ' + self.output_file)
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()

        logger.info(self.output_file + ' file has been created.')
        return self.output_file

    def __build_and_inject_analog(self, nwb_content):
        analog_directories = [single_dataset.get_data_path_from_dataset('analog') for single_dataset in self.datasets]
        analog_files = AnalogFiles(analog_directories)
        analog_manager = FlAnalogManager(
            analog_files=analog_files.get_files(),
            continuous_time_files=self.__get_continuous_time_files())
        fl_analog = analog_manager.get_analog()
        analog_injector = AnalogInjector(nwb_content)
        analog_injector.inject(AnalogCreator.create(fl_analog), 'behavior')

    def __build_and_inject_processing_module(self, nwb_content):
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

    def __build_and_inject_nwb_electrode_group(self, nwb_content, probes):
        logger.info('ElectrodeGroups: Building')
        fl_nwb_electrode_groups = self.fl_electrode_group_manager.get_fl_nwb_electrode_groups(probes)
        logger.info('ElectrodeGroups: Creating')
        nwb_electrode_groups = [self.nwb_electrode_group_creator.create_nwb_electrode_group(nwb_electrode_group)
                            for nwb_electrode_group in fl_nwb_electrode_groups]
        logger.info('ElectrodeGroups: Injecting into NWB')
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, nwb_electrode_groups)
        return nwb_electrode_groups

    def __build_and_inject_electrodes(self, nwb_content, electrode_groups):
        logger.info('Electrodes: Building')
        fl_electrodes = self.fl_electrode_manager.get_fl_electrodes(electrode_groups)
        logger.info('Electrodes: Creating&Injecting into NWB')
        [self.electrode_creator.create(nwb_content, fl_electrode) for fl_electrode in fl_electrodes]

    def __build_and_inject_electrodes_extensions(self, nwb_content):
        logger.info('ElectrodesExtensions: Building')
        electrodes_metadata_extension, electrodes_header_extension, electrodes_ntrode_extension_ntrode_id, electrodes_ntrode_extension_bad_channels = \
            self.electrode_extension_creator.create()

        logger.info('ElectrodesExtensions: Injecting into NWB')
        self.electrode_extension_injector.inject_extensions(
            nwb_content,
            electrodes_metadata_extension,
            electrodes_header_extension,
            electrodes_ntrode_extension_ntrode_id,
            electrodes_ntrode_extension_bad_channels
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
            self.header.configuration.hardware_configuration.sampling_rate,
            self.datasets
        )
        MdaInjector.inject_mda(nwb_content=nwb_content,
                               electrical_series=ElectricalSeriesCreator.create_mda(fl_mda_manager.get_data()))

    def __build_and_inject_epochs(self, nwb_content):
        logger.info('Epochs: Building')
        fl_epochs_manager = FlEpochsManager(self.datasets)
        epochs = fl_epochs_manager.get_epochs()
        EpochsInjector.inject(epochs, nwb_content)
