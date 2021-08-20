import logging.config
import os
import shutil
from datetime import datetime

import pytz
from rec_to_binaries import extract_trodes_rec_file
from rec_to_nwb.processing.builder.nwb_file_builder import NWBFileBuilder
from rec_to_nwb.processing.header.reconfig_header_checker import \
    ReconfigHeaderChecker
from rec_to_nwb.processing.metadata.metadata_manager import MetadataManager
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.validation.not_empty_validator import \
    NotEmptyValidator
from rec_to_nwb.processing.validation.validation_registrator import \
    ValidationRegistrator

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(
    fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_DEFAULT_LFP_EXPORT_ARGS = ('-highpass', '0', '-lowpass', '400',
                            '-interp', '0', '-userefs', '0',
                            '-outputrate', '1500')
_DEFAULT_MDA_EXPORT_ARGS = ('-usespikefilters', '0',
                            '-interp', '0', '-userefs', '0')

_DEFAULT_ANALOG_EXPORT_ARGS = ()
_DEFAULT_DIO_EXPORT_ARGS = ()
_DEFAULT_SPIKE_EXPORT_ARGS = ()
_DEFAULT_TIME_EXPORT_ARGS = ()

_DEFAULT_TRODES_REC_EXPORT_ARGS = ()

# temporary default value, for old dataset only
_DEFAULT_SESSION_START_TIME = datetime.fromtimestamp(
    0, pytz.utc)  # dummy value for now


class RawToNWBBuilder:
    """Unpack data from raw folder specified by arguments, and write those data into NWB file format

    Args:
        data_path  (string): path to directory containing all experiments data
        animal_name (string): directory name which represents animal subject of experiment
        dates (list of strings): dates of experiments on above animal
        nwb_metadata (MetadataManager): object containig metadata about experiment
        output_path (string): path and name specifying where .nwb file gonna be written
        video_path (string): path to directory with video files associated to nwb file
        extract_analog (boolean): flag if analog data should be extracted and processed from raw data
        extract_spikes (boolean): flag if spikes data should be extracted and processed from raw data
        extract_lfps (boolean): flag  if lfps data should be extracted and processed from raw data
        extract_dio (boolean): flag if dio data should be extracted and processed from raw data
        extract_mda (boolean): flag if mda data should be extracted and processed from raw data
        overwrite (boolean): flag if current extracted data in preprocessed folder content should be overwritten
        lfp_export_args (tuple of strings): parameters to launch lfp extraction from spikegadgets
        mda_export_args (tuple of strings): parameters to launch mda extraction from spikegadgets
        dio_export_args (tuple of strings): parameters to launch dio extraction from spikegadgets
        analog_export_args (tuple of strings): parameters to launch analog extraction from spikegadgets
        spikes_export_args (tuple of strings): parameters to launch spikes extraction from spikegadgets
        time_export_args (tuple of strings): parameters to launch time extraction from spikegadgets
        trodes_rec_export_args (tuple of strings): parameters to launch analog extraction from spikegadgets
        parallel_instances (int): number of parallel processes used during extracting data

    Methods:
        build_nwb()
        append_to_nwb()
        cleanup()
    """

    @beartype
    def __init__(
            self,
            data_path: str,
            animal_name: str,
            dates: list,
            nwb_metadata: MetadataManager,
            output_path: str = '',
            video_path: str = '',
            preprocessing_path: str = '',
            extract_analog: bool = True,
            extract_spikes: bool = False,
            extract_lfps: bool = False,
            extract_dio: bool = True,
            extract_mda: bool = True,
            overwrite: bool = True,
            lfp_export_args: tuple = _DEFAULT_LFP_EXPORT_ARGS,
            mda_export_args: tuple = _DEFAULT_MDA_EXPORT_ARGS,
            analog_export_args: tuple = _DEFAULT_ANALOG_EXPORT_ARGS,
            dio_export_args: tuple = _DEFAULT_DIO_EXPORT_ARGS,
            time_export_args: tuple = _DEFAULT_TIME_EXPORT_ARGS,
            spikes_export_args: tuple = _DEFAULT_SPIKE_EXPORT_ARGS,
            parallel_instances: int = 4,
            trodes_rec_export_args: tuple = _DEFAULT_TRODES_REC_EXPORT_ARGS
    ):

        validation_registrator = ValidationRegistrator()
        validation_registrator.register(NotEmptyValidator(data_path))
        validation_registrator.register(NotEmptyValidator(animal_name))
        validation_registrator.register(NotEmptyValidator(dates))
        validation_registrator.validate()

        self.extract_analog = extract_analog
        self.extract_spikes = extract_spikes
        self.extract_dio = extract_dio
        self.extract_lfps = extract_lfps
        self.extract_mda = extract_mda
        self.lfp_export_args = lfp_export_args + trodes_rec_export_args
        self.mda_export_args = mda_export_args + trodes_rec_export_args
        self.analog_export_args = analog_export_args + trodes_rec_export_args
        self.dio_export_args = dio_export_args + trodes_rec_export_args
        self.time_export_args = time_export_args + trodes_rec_export_args
        self.spikes_export_args = spikes_export_args + trodes_rec_export_args
        self.overwrite = overwrite
        self.animal_name = animal_name
        self.data_path = data_path
        self.dates = dates
        self.metadata = nwb_metadata.metadata
        self.output_path = output_path
        self.video_path = video_path
        if not preprocessing_path:
            self.preprocessing_path = data_path
        else:
            self.preprocessing_path = preprocessing_path
        self.probes = nwb_metadata.probes
        self.nwb_metadata = nwb_metadata
        self.parallel_instances = parallel_instances
        self.trodes_rec_export_args = trodes_rec_export_args

        self.is_old_dataset = self.__is_old_dataset()

    def __repr__(self):
        return ("RawToNWBBuilder(\n"
                f"    animal_name={self.animal_name},\n"
                f"    data_path={self.data_path},\n"
                f"    dates={self.dates},\n"
                f"    overwrite={self.overwrite},\n"
                f"    output_path={self.output_path},\n"
                f"    video_path={self.video_path},\n"
                f"    trodes_rec_export_args={self.trodes_rec_export_args},\n"
                ")")

    def __is_rec_config_valid(self):
        """ Check if XML is valid with XSD file """

        xml_file_path = self.__get_header_path()

        # ReconfigHeaderChecker.validate(xml_file_path)

        return xml_file_path

    def __get_header_path(self):
        xml_file_path = ''
        for counter, export_arg in enumerate(self.trodes_rec_export_args):
            if export_arg == '-reconfig':
                xml_file_path = self.trodes_rec_export_args[counter + 1]
        return xml_file_path

    def __is_old_dataset(self):
        # check raw directory for the single (first) date
        all_files = os.listdir(self.data_path + "/"
                               + self.animal_name + "/raw/"
                               + self.dates[0] + "/")
        if any([('videoTimeStamps.cameraHWSync' in file) for file in all_files]):
            # has cameraHWSync files; new dataset
            return False
        if any([('videoTimeStamps.cameraHWFrameCount' in file) for file in all_files]):
            # has cameraHWFrameCount files instead; old dataset
            logger.info('Seems to be an old dataset (no PTP)')
            return True
        raise FileNotFoundError(
            'need either cameraHWSync or cameraHWFrameCount files.')

    def build_nwb(self, run_preprocessing=True,
                  process_mda_valid_time=True, process_mda_invalid_time=True,
                  process_pos_valid_time=True, process_pos_invalid_time=True):
        """Builds nwb file for experiments from given dates.

        Args:
            process_mda_valid_time (boolean): True if the mda valid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True)
            process_mda_invalid_time (boolean): True if the mda invalid times should be build and append to nwb.
                Need the mda data inside the nwb. (default True)
            process_pos_valid_time (boolean): True if the pos valid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True)
            process_pos_invalid_time (boolean): True if the pos invalid times should be build and append to nwb.
                Need the pos data inside the nwb. (default True)
        """

        if run_preprocessing:
            self.__preprocess_data()

        self.__build_nwb_file(process_mda_valid_time=process_mda_valid_time,
                              process_mda_invalid_time=process_mda_invalid_time,
                              process_pos_valid_time=process_pos_valid_time,
                              process_pos_invalid_time=process_pos_invalid_time)

    def __build_nwb_file(self, process_mda_valid_time=False, process_mda_invalid_time=False,
                         process_pos_valid_time=False, process_pos_invalid_time=False):
        logger.info('Building NWB files')
        os.makedirs(self.output_path, exist_ok=True)
        os.makedirs(self.video_path, exist_ok=True)
        for date in self.dates:
            logger.info('Date: {}'.format(date))
            nwb_builder = self.get_nwb_builder(date)
            content = nwb_builder.build()
            nwb_builder.write(content)
            if self.is_old_dataset:
                logger.info('(old dataset: skipping append_to_nwb)')
                continue
            # self.append_to_nwb(
            #     nwb_builder=nwb_builder,
            #     process_mda_valid_time=process_mda_valid_time,
            #     process_mda_invalid_time=process_mda_invalid_time,
            #     process_pos_valid_time=process_pos_valid_time,
            #     process_pos_invalid_time=process_pos_invalid_time
            # )

    def get_nwb_builder(self, date):
        if self.is_old_dataset:
            old_dataset_kwargs = dict(is_old_dataset=True,
                                      session_start_time=_DEFAULT_SESSION_START_TIME)
        else:
            old_dataset_kwargs = dict()

        return NWBFileBuilder(
            data_path=self.data_path,
            animal_name=self.animal_name,
            date=date,
            nwb_metadata=self.nwb_metadata,
            output_file=self.output_path + self.animal_name + date + ".nwb",
            process_mda=self.extract_mda,
            process_dio=self.extract_dio,
            process_analog=self.extract_analog,
            preprocessing_path=self.preprocessing_path,
            video_path=self.video_path,
            reconfig_header=self.__get_header_path(),
            # reconfig_header=self.__is_rec_config_valid()
            **old_dataset_kwargs
        )

    def __preprocess_data(self):
        """process data with rec_to_binaries library"""

        logger.info(
            'Extraction parameters :' + '\n'
            + 'data_path = ' + self.data_path + '\n'
            + 'animal_name = ' + self.animal_name + '\n'
            + 'parallel_instances = ' + str(self.parallel_instances) + '\n'
            + 'extract_analog = ' + str(self.extract_analog) + '\n'
            + 'extract_dio = ' + str(self.extract_dio) + '\n'
            + 'extract_time = ' + str(True) + '\n'
            + 'extract_mda = ' + str(self.extract_mda) + '\n'
            + 'extract_lfps = ' + str(self.extract_lfps) + '\n'
            + 'extract_spikes = ' + str(self.extract_spikes) + '\n'
            + 'overwrite = ' + str(self.overwrite) + '\n'
            + 'lfp_export_args = ' + str(self.lfp_export_args) + '\n'
            + 'mda_export_args = ' + str(self.mda_export_args) + '\n'
            + 'analog_export_args = ' + str(self.analog_export_args) + '\n'
            + 'time_export_args = ' + str(self.time_export_args) + '\n'
            + 'spikes_export_args = ' + str(self.spikes_export_args) + '\n'
            + 'dio_export_args = ' + str(self.dio_export_args) + '\n'
            + 'trodes_rec_export_args = ' +
            str(self.trodes_rec_export_args) + '\n'
        )

        extract_trodes_rec_file(
            self.data_path,
            self.animal_name,
            out_dir=self.preprocessing_path,
            dates=self.dates,
            parallel_instances=self.parallel_instances,
            extract_analog=self.extract_analog,
            extract_dio=self.extract_dio,
            extract_time=True,
            extract_mda=self.extract_mda,
            extract_lfps=self.extract_lfps,
            extract_spikes=self.extract_spikes,
            overwrite=self.overwrite,
            lfp_export_args=self.lfp_export_args,
            mda_export_args=self.mda_export_args,
            analog_export_args=self.analog_export_args,
            dio_export_args=self.dio_export_args,
            spikes_export_args=self.spikes_export_args,
            time_export_args=self.time_export_args,
        )
        # self.__is_rec_config_valid()

    @staticmethod
    def append_to_nwb(nwb_builder, process_mda_valid_time, process_mda_invalid_time,
                      process_pos_valid_time, process_pos_invalid_time):
        """Append to NWBFile that was build using NWBFileBuilder passed in parameter.

        Args:
            nwb_builder (NWBFileBuilder): Builder that created NWBFile you want to append to
            process_mda_valid_time (boolean): If true, build and inject into NWB mda valid times
            process_mda_invalid_time (boolean): If true, build and inject into NWB mda invalid times
            process_pos_valid_time (boolean): If true, build and inject into NWB pos valid times
            process_pos_invalid_time (boolean): If true, build and inject into NWB pos invalid times
        """

        nwb_builder.build_and_append_to_nwb(
            process_mda_valid_time=process_mda_valid_time,
            process_mda_invalid_time=process_mda_invalid_time,
            process_pos_valid_time=process_pos_valid_time,
            process_pos_invalid_time=process_pos_invalid_time
        )

    def cleanup(self):
        """Remove all temporary files structure from preprocessing folder"""

        preprocessing = self.preprocessing_path + \
            '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)
