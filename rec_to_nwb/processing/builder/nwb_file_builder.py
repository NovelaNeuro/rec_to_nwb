import logging.config
import os
import uuid
from datetime import datetime

import pytz
from pynwb import NWBHDF5IO, NWBFile
from pynwb.file import Subject

from rec_to_nwb.processing.builder.originators.analog_originator import AnalogOriginator
from rec_to_nwb.processing.builder.originators.associated_files_originator import AssociatedFilesOriginator
from rec_to_nwb.processing.builder.originators.camera_device_originator import CameraDeviceOriginator
from rec_to_nwb.processing.builder.originators.camera_sample_frame_counts_originator import \
    CameraSampleFrameCountsOriginator
from rec_to_nwb.processing.builder.originators.data_acq_device_originator import DataAcqDeviceOriginator
from rec_to_nwb.processing.builder.originators.dio_originator import DioOriginator
from rec_to_nwb.processing.builder.originators.electrode_group_originator import ElectrodeGroupOriginator
from rec_to_nwb.processing.builder.originators.electrodes_extension_originator import ElectrodesExtensionOriginator
from rec_to_nwb.processing.builder.originators.electrodes_originator import ElectrodesOriginator
from rec_to_nwb.processing.builder.originators.epochs_originator import EpochsOriginator
from rec_to_nwb.processing.builder.originators.header_device_originator import HeaderDeviceOriginator
from rec_to_nwb.processing.builder.originators.mda_invalid_time_originator import MdaInvalidTimeOriginator
from rec_to_nwb.processing.builder.originators.mda_originator import MdaOriginator
from rec_to_nwb.processing.builder.originators.mda_valid_time_originator import MdaValidTimeOriginator
from rec_to_nwb.processing.builder.originators.pos_invalid_originator import PosInvalidTimeOriginator
from rec_to_nwb.processing.builder.originators.pos_valid_time_originator import PosValidTimeOriginator
from rec_to_nwb.processing.builder.originators.position_originator import PositionOriginator
from rec_to_nwb.processing.builder.originators.probe_originator import ProbeOriginator
from rec_to_nwb.processing.builder.originators.processing_module_originator import ProcessingModuleOriginator
from rec_to_nwb.processing.builder.originators.sample_count_timestamp_corespondence_originator import \
    SampleCountTimestampCorespondenceOriginator
from rec_to_nwb.processing.builder.originators.shanks_electrodes_originator import ShanksElectrodeOriginator
from rec_to_nwb.processing.builder.originators.shanks_originator import ShanksOriginator
from rec_to_nwb.processing.builder.originators.task_originator import TaskOriginator
from rec_to_nwb.processing.builder.originators.video_files_originator import VideoFilesOriginator
from rec_to_nwb.processing.header.header_checker.header_processor import HeaderProcessor
from rec_to_nwb.processing.header.header_checker.rec_file_finder import RecFileFinder
from rec_to_nwb.processing.header.module.header import Header
from rec_to_nwb.processing.metadata.corrupted_data_manager import CorruptedDataManager
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.nwb.common.session_time_extractor import SessionTimeExtractor
from rec_to_nwb.processing.nwb.components.device.device_factory import DeviceFactory
from rec_to_nwb.processing.nwb.components.device.device_injector import DeviceInjector
from rec_to_nwb.processing.nwb.components.device.probe.fl_probe_manager import FlProbeManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.data_scanner import DataScanner
from rec_to_nwb.processing.validation.associated_files_validator import AssociatedFilesExistanceValidator
from rec_to_nwb.processing.validation.metadata_section_validator import MetadataSectionValidator
from rec_to_nwb.processing.validation.ntrode_validator import NTrodeValidator
from rec_to_nwb.processing.validation.path_validator import PathValidator
from rec_to_nwb.processing.validation.preprocessing_validator import PreprocessingValidator
from rec_to_nwb.processing.validation.task_validator import TaskValidator
from rec_to_nwb.processing.validation.validation_registrator import ValidationRegistrator

path = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NWBFileBuilder:
    """Unpack data from preprocessing folder specified by arguments, and write those data into NWB file format

    Args:
        data_path (string): path to directory containing all experiments data
        animal_name (string): directory name which represents animal subject of experiment
        date (string): date of experiment
        nwb_metadata (MetadataManager): object contains metadata about experiment
        process_dio (boolean): flag if dio data should be processed
        process_mda (boolean): flag if mda data should be processed
        process_analog (boolean): flag if analog data should be processed
        video_path (string): path to directory with video files associated to nwb file
        output_file (string): path and name specifying where .nwb file gonna be written

    Methods:
        build()
        write()
        build_and_append_to_nwb()
    """

    @beartype
    def __init__(
            self,
            data_path: str,
            animal_name: str,
            date: str,
            nwb_metadata: MetadataManager,
            process_dio: bool = True,
            process_mda: bool = True,
            process_analog: bool = True,
            process_pos_timestamps: bool = True,
            video_path: str = '',
            output_file: str = 'output.nwb',
            reconfig_header: str = ''
    ):

        logger.info('NWBFileBuilder initialization')
        logger.info(
            'NWB builder initialization parameters: \n'
            + 'data_path = ' + str(data_path) + '\n'
            + 'animal_name = ' + str(animal_name) + '\n'
            + 'date = ' + str(date) + '\n'
            + 'nwb_metadata = ' + str(nwb_metadata) + '\n'
            + 'process_dio = ' + str(process_dio) + '\n'
            + 'process_mda = ' + str(process_mda) + '\n'
            + 'process_analog = ' + str(process_analog) + '\n'
            + 'output_file = ' + str(output_file) + '\n'
        )

        validation_registrator = ValidationRegistrator()
        validation_registrator.register(PathValidator(data_path))
        validation_registrator.validate()

        self.animal_name = animal_name
        self.date = date
        self.data_path = data_path
        self.metadata = nwb_metadata.metadata
        metadata_section_validator = MetadataSectionValidator(self.metadata)
        metadata_section_validator.validate_sections()
        if self.metadata.get('associated_files', []):
            associated_files_existance_validator = AssociatedFilesExistanceValidator(self.metadata['associated_files'])
            if associated_files_existance_validator.files_exist():
                pass
            else:
                raise Exception("one or more associated file listed in metadata.yaml file does not exist")
        self.probes = nwb_metadata.probes
        self.process_dio = process_dio
        self.process_mda = process_mda
        self.process_analog = process_analog
        self.process_pos_timestamps = process_pos_timestamps
        self.output_file = output_file
        self.video_path = video_path
        self.link_to_notes = self.metadata.get('link to notes', None)
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
        if reconfig_header:
            self.header = Header(reconfig_header)
        else:
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

        self.shanks_electrode_originator = ShanksElectrodeOriginator(self.probes, self.metadata)
        self.shanks_originator = ShanksOriginator(self.probes, self.metadata)

        self.fl_probe_manager = FlProbeManager(self.probes)
        self.device_injector = DeviceInjector()
        self.device_factory = DeviceFactory()

        self.electrode_group_originator = ElectrodeGroupOriginator(self.metadata)
        self.electrodes_originator = ElectrodesOriginator(self.probes, self.metadata)

        self.session_time_extractor = SessionTimeExtractor(
            self.datasets,
            self.animal_name,
            self.date,
            self.dataset_names
        )

        self.mda_valid_time_originator = MdaValidTimeOriginator(self.header, self.metadata)
        self.mda_invalid_time_originator = MdaInvalidTimeOriginator(self.header, self.metadata)
        self.pos_valid_time_originator = PosValidTimeOriginator(self.metadata)
        self.pos_invalid_time_originator = PosInvalidTimeOriginator(self.metadata)

        self.epochs_originator = EpochsOriginator(self.datasets)

        if 'associated_files' in self.metadata:
            self.associated_files_originator = AssociatedFilesOriginator(self.metadata)

        self.electrodes_extension_originator = ElectrodesExtensionOriginator(
            self.probes,
            self.metadata,
            self.header
        )

        self.sample_count_timestamp_corespondence_originator =\
            SampleCountTimestampCorespondenceOriginator(self.datasets)
        self.processing_module_originator = ProcessingModuleOriginator()
        self.task_originator = TaskOriginator(self.metadata)
        self.camera_device_originator = CameraDeviceOriginator(self.metadata)
        self.header_device_originator = HeaderDeviceOriginator(self.header, self.metadata)
        self.probes_originator = ProbeOriginator(self.device_factory, self.device_injector, self.probes)
        self.camera_sample_frame_counts_originator = CameraSampleFrameCountsOriginator(
            self.data_path + "/" + animal_name + "/raw/" + self.date + "/")
        self.video_files_originator = VideoFilesOriginator(
            self.data_path + "/" + animal_name + "/raw/" + self.date + "/",
            self.video_path,
            self.metadata["associated_video_files"],
        )

        self.data_acq_device_originator = DataAcqDeviceOriginator(
            device_factory=self.device_factory,
            device_injector=self.device_injector,
            metadata=self.metadata['data acq device']
        )

        if self.process_mda:
            self.mda_originator = MdaOriginator(self.datasets, self.header, self.metadata)

        if self.process_dio:
            self.dio_originator = DioOriginator(self.metadata, self.datasets)

        if self.process_analog:
            self.analog_originator = AnalogOriginator(self.datasets, self.metadata)

        self.position_originator = PositionOriginator(self.datasets, self.metadata,
                                                      self.dataset_names, self.process_pos_timestamps)

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

        self.processing_module_originator.make(nwb_content)

 
        if 'associated_files' in self.metadata:
            self.associated_files_originator.make(nwb_content)

        self.position_originator.make(nwb_content)

        valid_map_dict = self.__build_corrupted_data_manager()

        shanks_electrodes_dict = self.shanks_electrode_originator.make()

        shanks_dict = self.shanks_originator.make(shanks_electrodes_dict)

        probes = self.probes_originator.make(nwb_content, shanks_dict, valid_map_dict['probes'])

        self.data_acq_device_originator.make(nwb_content)

        self.header_device_originator.make(nwb_content)

        self.camera_device_originator.make(nwb_content)

        self.video_files_originator.make(nwb_content)

        electrode_groups = self.electrode_group_originator.make(
            nwb_content, probes, valid_map_dict['electrode_groups']
        )

        self.electrodes_originator.make(
            nwb_content, electrode_groups, valid_map_dict['electrodes'], valid_map_dict['electrode_groups']
        )

        self.electrodes_extension_originator.make(nwb_content, valid_map_dict['electrodes'])

        self.epochs_originator.make(nwb_content)

        self.sample_count_timestamp_corespondence_originator.make(nwb_content)

        self.task_originator.make(nwb_content)

        self.camera_sample_frame_counts_originator.make(nwb_content)

        if self.process_dio:
            self.dio_originator.make(nwb_content)

        if self.process_mda:
            self.mda_originator.make(nwb_content)

        if self.process_analog:
            self.analog_originator.make(nwb_content)


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

    def build_and_append_to_nwb(self, process_mda_valid_time=True, process_mda_invalid_time=True,
                                process_pos_valid_time=True, process_pos_invalid_time=True):
        """Create and append to existing nwb. Set flag to add it to nwb

        Args:
            process_mda_valid_time (boolean): True if the mda valid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True)
            process_mda_invalid_time (boolean): True if the mda invalid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True)
            process_pos_valid_time (boolean): True if the pos valid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True)
            process_pos_invalid_time (boolean): True if the pos invalid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True)

        Raises:
            ElementExistException: If element already exist in NWB

        Returns:
            NWBFile: Return NWBFile content
        """

        with NWBHDF5IO(path=self.output_file, mode='a') as nwb_file_io:
            nwb_content = nwb_file_io.read()

            if self.process_pos_timestamps:
                if process_pos_valid_time:
                    self.pos_valid_time_originator.make(nwb_content)
                if process_pos_invalid_time:
                    self.pos_invalid_time_originator.make(nwb_content)

            if process_mda_valid_time:
                self.mda_valid_time_originator.make(nwb_content)
            if process_mda_invalid_time:
                self.mda_invalid_time_originator.make(nwb_content)


            nwb_file_io.write(nwb_content)
