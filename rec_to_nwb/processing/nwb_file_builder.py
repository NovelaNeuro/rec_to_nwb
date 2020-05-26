import logging.config
import os
import uuid
from datetime import datetime

import pytz
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

from rec_to_nwb.processing.header.header_checker.header_processor import HeaderProcessor
from rec_to_nwb.processing.header.header_checker.rec_file_finder import RecFileFinder
from rec_to_nwb.processing.header.module.header import Header
from rec_to_nwb.processing.metadata.corrupted_data_manager import CorruptedDataManager
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.nwb.common.session_time_extractor import SessionTimeExtractor
from rec_to_nwb.processing.nwb.components.analog.analog_creator import AnalogCreator
from rec_to_nwb.processing.nwb.components.analog.analog_files import AnalogFiles
from rec_to_nwb.processing.nwb.components.analog.analog_injector import AnalogInjector
from rec_to_nwb.processing.nwb.components.analog.fl_analog_manager import FlAnalogManager
from rec_to_nwb.processing.nwb.components.associated_files.associated_files_creator import AssociatedFilesCreator
from rec_to_nwb.processing.nwb.components.associated_files.associated_files_injector import AssociatedFilesInjector
from rec_to_nwb.processing.nwb.components.associated_files.fl_associated_files_manager import FlAssociatedFilesManager
from rec_to_nwb.processing.nwb.components.device.device_factory import DeviceFactory
from rec_to_nwb.processing.nwb.components.device.device_injector import DeviceInjector
from rec_to_nwb.processing.nwb.components.device.fl_device_header_manager import FlDeviceHeaderManager
from rec_to_nwb.processing.nwb.components.device.fl_probe_manager import FlProbeManager
from rec_to_nwb.processing.nwb.components.device.shanks.fl_shank_manager import FlShankManager
from rec_to_nwb.processing.nwb.components.device.shanks.shank_creator import ShankCreator
from rec_to_nwb.processing.nwb.components.device.shanks_electrodes.fl_shanks_electrode_manager import \
    FlShanksElectrodeManager
from rec_to_nwb.processing.nwb.components.device.shanks_electrodes.shanks_electrode_creator import \
    ShanksElectrodeCreator
from rec_to_nwb.processing.nwb.components.dio.dio_builder import DioBuilder
from rec_to_nwb.processing.nwb.components.dio.dio_files import DioFiles
from rec_to_nwb.processing.nwb.components.dio.dio_injector import DioInjector
from rec_to_nwb.processing.nwb.components.dio.dio_manager import DioManager
from rec_to_nwb.processing.nwb.components.electrode_group.electrode_group_factory import ElectrodeGroupFactory
from rec_to_nwb.processing.nwb.components.electrode_group.electrode_group_injector import ElectrodeGroupInjector
from rec_to_nwb.processing.nwb.components.electrode_group.fl_nwb_electrode_group_manager import \
    FlNwbElectrodeGroupManager
from rec_to_nwb.processing.nwb.components.electrodes.electrode_creator import ElectrodesCreator
from rec_to_nwb.processing.nwb.components.electrodes.extension.electrode_extension_injector import \
    ElectrodeExtensionInjector
from rec_to_nwb.processing.nwb.components.electrodes.extension.fl_electrode_extension_manager import \
    FlElectrodeExtensionManager
from rec_to_nwb.processing.nwb.components.electrodes.fl_electrode_manager import FlElectrodeManager
from rec_to_nwb.processing.nwb.components.epochs.epochs_injector import EpochsInjector
from rec_to_nwb.processing.nwb.components.epochs.fl_epochs_manager import FlEpochsManager
from rec_to_nwb.processing.nwb.components.mda.electrical_series_creator import ElectricalSeriesCreator
from rec_to_nwb.processing.nwb.components.mda.fl_mda_manager import FlMdaManager
from rec_to_nwb.processing.nwb.components.mda.mda_injector import MdaInjector
from rec_to_nwb.processing.nwb.components.mda.time.invalid.fl_mda_invalid_time_manager import FlMdaInvalidTimeManager
from rec_to_nwb.processing.nwb.components.mda.time.invalid.mda_invalid_time_injector import MdaInvalidTimeInjector
from rec_to_nwb.processing.nwb.components.mda.time.valid.fl_mda_valid_time_manager import FlMdaValidTimeManager
from rec_to_nwb.processing.nwb.components.mda.time.valid.mda_valid_time_injector import MdaValidTimeInjector
from rec_to_nwb.processing.nwb.components.position.fl_position_manager import FlPositionManager
from rec_to_nwb.processing.nwb.components.position.position_creator import PositionCreator
from rec_to_nwb.processing.nwb.components.position.time.invalid.fl_pos_invalid_time_manager import \
    FlPosInvalidTimeManager
from rec_to_nwb.processing.nwb.components.position.time.invalid.pos_invalid_time_injector import PosInvalidTimeInjector
from rec_to_nwb.processing.nwb.components.position.time.valid.fl_pos_valid_time_manager import FlPosValidTimeManager
from rec_to_nwb.processing.nwb.components.processing_module.processing_module_creator import ProcessingModuleCreator
from rec_to_nwb.processing.nwb.components.task.task_builder import TaskBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.data_scanner import DataScanner
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator
from rec_to_nwb.processing.validation.preprocessing_validator import PreprocessingValidator
from rec_to_nwb.processing.validation.task_validator import TaskValidator
from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NWBFileBuilder:
    """Unpack data from preprocessing folder specified by arguments, and write those data into NWB file format

    Args:
        data_path (string): path to directory containing all experiments data
        animal_name (string): directory name which represents animal subject of experiment
        date (string): date of experiment
        nwb_metadata (MetadataManager): object contains metadata about experiment
        associated_files (list of strings): list of paths to files stored inside nwb
        process_dio (boolean): flag if dio data should be processed
        process_mda (boolean): flag if mda data should be processed
        process_analog (boolean): flag if analog data should be processed
        process_mda_valid_times (boolean): flag if mda valid times should be processed
        process_mda_invalid_times (boolean): flag if mda invalid times should be processed
        process_pos_valid_times (boolean): flag if pos valid times should be processed
        process_pos_invalid_times (boolean): flag if pos invalid times should be processed
        output_file (string): path and name specifying where .nwb file gonna be written

    Methods:
        build()
        write()
    """

    @beartype
    def __init__(
            self,
            data_path: str,
            animal_name: str,
            date: str,
            nwb_metadata: MetadataManager,
            associated_files: list = [],
            process_dio: bool = True,
            process_mda: bool = True,
            process_analog: bool = True,
            process_mda_valid_times: bool = False,
            process_mda_invalid_times: bool = False,
            process_pos_valid_times: bool = False,
            process_pos_invalid_times: bool = False,
            output_file: str = 'output.nwb'
    ):

        logger.info('NWBFileBuilder initialization')
        logger.info(
            'NWB builder initialization parameters: \n'
            + 'data_path = ' + str(data_path) + '\n'
            + 'animal_name = ' + str(animal_name) + '\n'
            + 'date = ' + str(date) + '\n'
            + 'nwb_metadata = ' + str(nwb_metadata) + '\n'
            + 'associated_files = ' + str(associated_files) + '\n'
            + 'process_dio = ' + str(process_dio) + '\n'
            + 'process_mda = ' + str(process_mda) + '\n'
            + 'process_analog = ' + str(process_analog) + '\n'
            + 'output_file = ' + str(output_file) + '\n'
        )

        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.metadata = nwb_metadata.metadata
        self.associated_files = associated_files
        self.probes = nwb_metadata.probes
        self.process_dio = process_dio
        self.process_mda = process_mda
        self.process_analog = process_analog
        self.process_mda_valid_times = process_mda_valid_times
        self.process_mda_invalid_times = process_mda_invalid_times
        self.process_pos_valid_times = process_pos_valid_times
        self.process_pos_invalid_times = process_pos_invalid_times
        self.output_file = output_file
        self.link_to_notes = self.metadata.get('link to notes', '')
        data_types_for_scanning = {'pos': True,
                                   'time': True,
                                   'mda': process_mda,
                                   'DIO': process_dio,
                                   'analog': process_analog}

        rec_files_list = RecFileFinder().find_rec_files(
            path=(self.data_path
                  + '/' + self.animal_name
                  + '/raw/'
                  + self.date)
        )
        header_file = HeaderProcessor.process_headers(rec_files_list)
        self.header = Header(header_file)
        self.data_scanner = DataScanner(data_path, animal_name, nwb_metadata)
        self.dataset_names = self.data_scanner.get_all_epochs(date)
        full_data_path = data_path + '/' + animal_name + '/preprocessing/' + date

        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NTrodeValidator(self.metadata, self.header, self.probes))
        validation_registrator.register(PreprocessingValidator(
            full_data_path,
            self.dataset_names,
            data_types_for_scanning
        ))
        validation_registrator.register(TaskValidator(self.metadata['tasks']))
        validation_registrator.validate()

        self.__extract_datasets(animal_name, date)

        self.corrupted_data_manager = CorruptedDataManager(self.metadata)

        self.pm_creator = ProcessingModuleCreator('behavior', 'Contains all behavior-related data')

        self.task_builder = TaskBuilder(self.metadata)

        self.fl_position_manager = FlPositionManager(self.datasets, str(self.metadata['meters_per_pixel']))
        self.position_creator = PositionCreator()

        self.fl_shanks_electrode_manager = FlShanksElectrodeManager(self.probes, self.metadata['electrode groups'])
        self.shanks_electrodes_creator = ShanksElectrodeCreator()

        self.fl_shank_manager = FlShankManager(self.probes, self.metadata['electrode groups'])
        self.shank_creator = ShankCreator()

        self.fl_probe_manager = FlProbeManager(self.probes)
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

        self.fl_device_header_manager = FlDeviceHeaderManager(
            'header_device',
            self.header.configuration.global_configuration
        )

        self.fl_nwb_electrode_group_manager = FlNwbElectrodeGroupManager(self.metadata['electrode groups'])
        self.electrode_group_creator = ElectrodeGroupFactory()
        self.electrode_group_injector = ElectrodeGroupInjector()

        self.fl_electrode_manager = FlElectrodeManager(self.probes, self.metadata['electrode groups'])
        self.electrode_creator = ElectrodesCreator()

        self.fl_electrode_extension_manager = FlElectrodeExtensionManager(
            self.probes,
            self.metadata,
            self.header
        )
        self.electrode_extension_injector = ElectrodeExtensionInjector()

        if associated_files:
            self.fl_associated_files_manager = FlAssociatedFilesManager(
                self.associated_files,
                self.metadata['associated_files']
            )
            self.associated_files_creator = AssociatedFilesCreator()
            self.associated_files_injector = AssociatedFilesInjector()

        self.session_time_extractor = SessionTimeExtractor(
            self.datasets,
            self.animal_name,
            self.date,
            self.dataset_names
        )

        self.fl_mda_valid_time_manager = FlMdaValidTimeManager(
            sampling_rate=float(self.header.configuration.hardware_configuration.sampling_rate),
        )
        self.mda_valid_time_injector = MdaValidTimeInjector()

        self.fl_mda_invalid_time_manager = FlMdaInvalidTimeManager(
            sampling_rate=float(self.header.configuration.hardware_configuration.sampling_rate),
        )
        self.mda_invalid_time_injector = MdaInvalidTimeInjector()

        self.fl_pos_valid_time_manager = FlPosValidTimeManager()
        self.pos_valid_time_injector = MdaValidTimeInjector()

        self.fl_pos_invalid_time_manager = FlPosInvalidTimeManager()
        self.pos_invalid_time_injector = PosInvalidTimeInjector()

    def __extract_datasets(self, animal_name, date):
        self.data_scanner.extract_data_from_date_folder(date)
        self.datasets = [self.data_scanner.data[animal_name][date][dataset] for dataset in self.dataset_names]

    def build(self):
        """Build NWBFile

        Returns:
              NWBFile: Return NWBFile content
        """

        logger.info('Building components for NWB')
        nwb_content = NWBFile(
            session_description=self.metadata['session description'],
            experimenter=self.metadata['experimenter name'],
            lab=self.metadata['lab'],
            institution=self.metadata['institution'],
            session_start_time=self.session_time_extractor.get_session_start_time(),
            timestamps_reference_time=datetime.fromtimestamp(0, pytz.utc),
            identifier=str(uuid.uuid1()),
            session_id=self.metadata['session_id'],
            notes=self.link_to_notes,
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

        valid_map_dict = self.__build_corrupted_data_manager()

        self.__build_and_inject_processing_module(nwb_content)

        shanks_electrodes_dict = self.__build_shanks_electrodes()

        shanks_dict = self.__build_shanks(shanks_electrodes_dict)

        probes = self.__build_and_inject_probes(nwb_content, shanks_dict, valid_map_dict['probes'])

        self.__build_and_inject_header_device(nwb_content)

        electrode_groups = self.__build_and_inject_electrode_group(
            nwb_content, probes, valid_map_dict['electrode_groups']
        )

        self.__build_and_inject_electrodes(
            nwb_content, electrode_groups, valid_map_dict['electrodes'], valid_map_dict['electrode_groups']
        )

        self.__build_and_inject_electrodes_extensions(nwb_content, valid_map_dict['electrodes'])

        self.__build_and_inject_epochs(nwb_content)

        if self.associated_files:
            self.__build_and_inject_associated_files(nwb_content)

        if self.process_dio:
            self.__build_and_inject_dio(nwb_content)

        if self.process_mda:
            self.__build_and_inject_mda(nwb_content)

            if self.process_mda_valid_times:
                self.__build_and_inject_mda_valid_times(nwb_content)

            if self.process_mda_invalid_times:
                self.__build_and_inject_mda_invalid_times(nwb_content)

        if self.process_analog:
            self.__build_and_inject_analog(nwb_content)

        if self.process_pos_valid_times:
            self.__build_and_inject_pos_valid_times(nwb_content)

        if self.process_pos_invalid_times:
            self.__build_and_inject_pos_invalid_times(nwb_content)

        return nwb_content

    def write(self, content):
        """Write nwb file handler with colected data into actual file"""

        logger.info('Writing down content to ' + self.output_file)
        with NWBHDF5IO(path=self.output_file, mode='w') as nwb_fileIO:
            nwb_fileIO.write(content)
            nwb_fileIO.close()

        logger.info(self.output_file + ' file has been created.')
        return self.output_file

    def __build_corrupted_data_manager(self):
        logger.info('CorruptedData: Checking')
        return self.corrupted_data_manager.get_valid_map_dict()

    def __build_and_inject_analog(self, nwb_content):
        analog_directories = [single_dataset.get_data_path_from_dataset('analog') for single_dataset in self.datasets]
        analog_files = AnalogFiles(analog_directories)
        analog_manager = FlAnalogManager(
            analog_files=analog_files.get_files(),
            continuous_time_files=self.__get_continuous_time_files()
        )
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

    def __build_shanks_electrodes(self):
        logger.info('Probes-ShanksElectrode: Building')
        fl_shanks_electrodes_dict = self.fl_shanks_electrode_manager.get_fl_shanks_electrodes_dict()
        logger.info('Probes-ShanksElectrode: Creating')
        shanks_electrodes_dict = {}
        for probe_type, fl_shanks_electrodes in fl_shanks_electrodes_dict.items():
            shanks_electrodes_dict[probe_type] = [
                self.shanks_electrodes_creator.create(fl_shanks_electrode)
                for fl_shanks_electrode in fl_shanks_electrodes
            ]
        return shanks_electrodes_dict

    def __build_shanks(self, shanks_electrodes_dict):
        logger.info('Probes-Shanks: Building')
        fl_shanks_dict = self.fl_shank_manager.get_fl_shanks_dict(shanks_electrodes_dict)
        logger.info('Probes-Shanks: Creating')
        shanks_dict = {}
        for probe_type, fl_shanks in fl_shanks_dict.items():
            shanks_dict[probe_type] = [self.shank_creator.create(fl_shank) for fl_shank in fl_shanks]
        return shanks_dict

    def __build_and_inject_probes(self, nwb_content, shanks_dict, probes_valid_map):
        logger.info('Probes: Building')
        fl_probes = self.fl_probe_manager.get_fl_probes(shanks_dict, probes_valid_map)
        logger.info('Probes: Creating probes')
        probes = [self.device_factory.create_probe(fl_probe) for fl_probe in fl_probes]
        logger.info('Probes: Injecting probes into NWB')
        self.device_injector.inject_all_devices(nwb_content, probes)
        return probes

    def __build_and_inject_electrode_group(self, nwb_content, probes, electrode_groups_valid_map):
        logger.info('ElectrodeGroups: Building')
        fl_nwb_electrode_groups = self.fl_nwb_electrode_group_manager.get_fl_nwb_electrode_groups(
            probes=probes,
            electrode_groups_valid_map=electrode_groups_valid_map
        )
        logger.info('ElectrodeGroups: Creating')
        nwb_electrode_groups = [
            self.electrode_group_creator.create_nwb_electrode_group(nwb_electrode_group)
            for nwb_electrode_group in fl_nwb_electrode_groups
        ]
        logger.info('ElectrodeGroups: Injecting into NWB')
        self.electrode_group_injector.inject_all_electrode_groups(nwb_content, nwb_electrode_groups)
        return nwb_electrode_groups

    def __build_and_inject_electrodes(self, nwb_content, electrode_groups, electrodes_valid_map,
                                      electrode_groups_valid_map):
        logger.info('Electrodes: Building')
        fl_electrodes = self.fl_electrode_manager.get_fl_electrodes(
            electrode_groups=electrode_groups,
            electrodes_valid_map=electrodes_valid_map,
            electrode_groups_valid_map=electrode_groups_valid_map
        )
        logger.info('Electrodes: Creating&Injecting into NWB')
        [self.electrode_creator.create(nwb_content, fl_electrode) for fl_electrode in fl_electrodes]

    def __build_and_inject_electrodes_extensions(self, nwb_content, electrodes_valid_map):
        logger.info('FlElectrodesExtensions: Building')
        fl_electrode_extension = self.fl_electrode_extension_manager.get_fl_electrodes_extension(electrodes_valid_map)
        logger.info('FlElectrodesExtensions: Injecting into NWB')
        self.electrode_extension_injector.inject_extensions(
            nwb_content,
            fl_electrode_extension
        )

    def __build_and_inject_dio(self, nwb_content):
        logger.info('DIO: Prepare directories')
        dio_directories = [single_dataset.get_data_path_from_dataset('DIO') for single_dataset in self.datasets]
        logger.info('DIO: Prepare files')
        dio_files = DioFiles(dio_directories, self.metadata['behavioral_events'])
        logger.info('DIO: Retrieve data')
        dio_manager = DioManager(
            dio_files=dio_files.get_files(),
            dio_metadata=self.metadata['behavioral_events'],
            continuous_time_files=self.__get_continuous_time_files()
        )
        dio_data = dio_manager.get_dio()
        logger.info('DIO: Building')
        dio_builder = DioBuilder(dio_data, self.metadata['behavioral_events'])
        behavioral_events = dio_builder.build()
        logger.info('DIO: Injecting into NWB')
        dio_injector = DioInjector(nwb_content)
        dio_injector.inject(behavioral_events, 'behavior')

    def __get_continuous_time_files(self):
        return [single_dataset.get_continuous_time() for single_dataset in self.datasets]

    def __build_and_inject_associated_files(self, nwb_content):
        logger.info('AssociatedFiles: Building')
        fl_associated_files = self.fl_associated_files_manager.get_fl_associated_files()
        logger.info('AssociatedFiles: Creating')
        associated_files = [
            self.associated_files_creator.create(fl_associated_file)
            for fl_associated_file in fl_associated_files
        ]
        logger.info('AssociatedFiles: Injecting')
        self.associated_files_injector.inject(associated_files, 'behavior', nwb_content)

    def __build_and_inject_mda(self, nwb_content):
        logger.info('MDA: Building')
        fl_mda_manager = FlMdaManager(
            nwb_content=nwb_content,
            sampling_rate=float(self.header.configuration.hardware_configuration.sampling_rate),
            datasets=self.datasets
        )
        fl_mda = fl_mda_manager.get_data()
        logger.info('MDA: Injecting')
        MdaInjector.inject_mda(
            nwb_content=nwb_content,
            electrical_series=ElectricalSeriesCreator.create_mda(fl_mda)
        )

    def __build_and_inject_epochs(self, nwb_content):
        logger.info('Epochs: Building')
        fl_epochs_manager = FlEpochsManager(self.datasets)
        logger.info('Epochs: Creating')
        epochs = fl_epochs_manager.get_epochs()
        logger.info('Epochs: Injecting')
        EpochsInjector.inject(epochs, nwb_content)

    def __build_and_inject_mda_valid_times(self, nwb_content):
        logger.info('MDA valid times: Building')
        mda_valid_times = self.fl_mda_valid_time_manager.get_fl_mda_valid_times(nwb_content)
        logger.info('MDA valid times: Injecting')
        self.mda_valid_time_injector.inject_all(mda_valid_times, nwb_content)

    def __build_and_inject_mda_invalid_times(self, nwb_content):
        logger.info('MDA invalid times: Building')
        mda_invalid_times = self.fl_mda_invalid_time_manager.get_fl_mda_invalid_times(nwb_content)
        logger.info('MDA invalid times: Injecting')
        self.mda_invalid_time_injector.inject_all(mda_invalid_times, nwb_content)

    def __build_and_inject_pos_valid_times(self, nwb_content):
        logger.info('POS valid times: Building')
        pos_valid_times = self.fl_pos_valid_time_manager.get_fl_pos_valid_times(nwb_content)
        logger.info('POS valid times: Injecting')
        self.pos_valid_time_injector.inject_all(pos_valid_times, nwb_content)

    def __build_and_inject_pos_invalid_times(self, nwb_content):
        logger.info('POS invalid times: Building')
        pos_invalid_times = self.fl_pos_invalid_time_manager.get_fl_pos_invalid_times(nwb_content)
        logger.info('POS invalid times: Injecting')
        self.pos_invalid_time_injector.inject_all(pos_invalid_times, nwb_content)

    def build_and_append_mda_valid_times(self):
        with NWBHDF5IO(path=self.output_file, mode='a') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            self.__build_and_inject_mda_valid_times(nwb_content)
            nwb_file_io.write(nwb_content)

    def build_and_append_mda_invalid_times(self):
        with NWBHDF5IO(path=self.output_file, mode='a') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            self.__build_and_inject_mda_invalid_times(nwb_content)
            nwb_file_io.write(nwb_content)

    def build_and_append_pos_valid_times(self):
        with NWBHDF5IO(path=self.output_file, mode='a') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            self.__build_and_inject_pos_valid_times(nwb_content)
            nwb_file_io.write(nwb_content)

    def build_and_append_pos_invalid_times(self):
        with NWBHDF5IO(path=self.output_file, mode='a') as nwb_file_io:
            nwb_content = nwb_file_io.read()
            self.__build_and_inject_pos_invalid_times(nwb_content)
            nwb_file_io.write(nwb_content)

# ToDo TImestamps.any()
# ToDo Maybe build_and_append_to_nwb(). We can pass in param string "mda_invalid_times" and function should do the rest.
# ToDo check if module exist
# ToDo Update readme
# ToDo check pylint - After few commit I test some other branch where I recreate env and as I see now,
#  I forgot install pylint. I will add it tomorrow
#     ToDo Period should be stored in NWBFileBuilder / metadata.yml
