import logging
import os
import shutil

from rec_to_binaries import extract_trodes_rec_file
import xmlschema

from fl.datamigration.metadata.metadata_manager import MetadataManager
from fl.datamigration.nwb_file_builder import NWBFileBuilder
from fl.datamigration.validation.not_empty_validator import NotEmptyValidator
from fl.datamigration.validation.type_validator import TypeValidator
from fl.datamigration.validation.export_args_validator import ExportArgsValidator
from fl.datamigration.validation.validation_registrator import ValidationRegistrator

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

_DEFAULT_LFP_EXPORT_ARGS = ('-highpass', '0', '-lowpass', '400',
                            '-interp', '0', '-userefs', '0',
                            '-outputrate', '1500')
_DEFAULT_MDA_EXPORT_ARGS = ('-usespikefilters', '0',
                            '-interp', '0', '-userefs', '0')

_DEFAULT_ANALOG_EXPORT_ARGS = ()


class RawToNWBBuilder:

    def __init__(
            self,
            data_path,
            animal_name,
            dates,
            nwb_metadata,
            output_path='',
            extract_analog=True,
            extract_spikes=False,
            extract_lfps=False,
            extract_dio=True,
            extract_mda=True,
            overwrite=True,
            lfp_export_args=_DEFAULT_LFP_EXPORT_ARGS,
            mda_export_args=_DEFAULT_MDA_EXPORT_ARGS,
            parallel_instances=4,
            analog_export_args=_DEFAULT_ANALOG_EXPORT_ARGS
    ):
        """
        Args:
        data_path  (string): path to directory containing all experiments data
        animal_name (string): directory name which represents animal subject of experiment
        dates (list of strings): dates of experiments on above animal
        nwb_metadata (MetadataManager): object containig metadata about experiment
        output_path (string): path and name specifying where .nwb file gonna be written
        extract_analog (boolean): flag if analog data should be extracted and processed from raw data
        extract_spikes (boolean): flag if spikes data should be extracted and processed from raw data
        extract_lfps (boolean): flag  if lfps data should be extracted and processed from raw data
        extract_dio (boolean): flag if dio data should be extracted and processed from raw data
        extract_mda (boolean): flag if mda data should be extracted and processed from raw data
        overwrite (boolean): flag if current extracted data in preprocessed folder content should be overwritten
        lfp_export_args (tuple of strings): parameters to launch lfp extraction from spikegadgets
        mda_export_args (tuple of strings): parameters to launch mda extraction from spikegadgets
        analog_export_args (tuple of strings): parameters to launch analog extraction from spikegadgets
        parallel_instances (int): number of parallel processes used during processing data
        """

        validationRegistrator = ValidationRegistrator()
        validationRegistrator.register(TypeValidator(data_path, str))
        validationRegistrator.register(NotEmptyValidator(data_path))
        validationRegistrator.register(TypeValidator(animal_name, str))
        validationRegistrator.register(NotEmptyValidator(animal_name))
        validationRegistrator.register(TypeValidator(dates, list))
        validationRegistrator.register(NotEmptyValidator(dates))
        validationRegistrator.register(TypeValidator(nwb_metadata, MetadataManager))
        validationRegistrator.register(TypeValidator(output_path, str))
        validationRegistrator.register(TypeValidator(extract_analog, bool))
        validationRegistrator.register(TypeValidator(extract_spikes, bool))
        validationRegistrator.register(TypeValidator(extract_lfps, bool))
        validationRegistrator.register(TypeValidator(extract_dio, bool))
        validationRegistrator.register(TypeValidator(extract_mda, bool))
        validationRegistrator.register(TypeValidator(overwrite, bool))
        validationRegistrator.register(TypeValidator(parallel_instances, int))
        validator_registrator.register(ExportArgsValidator(lfp_export_args))
        validator_registrator.register(ExportArgsValidator(mda_export_args))
        validator_registrator.register(ExportArgsValidator(analog_export_args))
        validator_registrator.validate()

        self.extract_analog = extract_analog
        self.extract_spikes = extract_spikes
        self.extract_dio = extract_dio
        self.extract_lfps = extract_lfps
        self.extract_mda = extract_mda
        self.lfp_export_args = lfp_export_args
        self.mda_export_args = mda_export_args
        self.overwrite = overwrite
        self.animal_name = animal_name
        self.data_path = data_path
        self.dates = dates
        self.metadata = nwb_metadata.metadata
        self.output_path = output_path
        self.probes = nwb_metadata.probes
        self.nwb_metadata = nwb_metadata
        self.parallel_instances = parallel_instances
        self.analog_export_args = analog_export_args

        if self.analog_export_args != ():
            if not self.__is_rec_config_valid():
                raise Exception('reconfig xml does not match expected xsd')

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
        )

        extract_trodes_rec_file(self.data_path,
                                self.animal_name,
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
                                analog_export_args=self.analog_export_args
                                )

    def build_nwb(self):
        """builds nwb file for experiments from given dates"""

        self.__preprocess_data()
        for date in self.dates:
            nwb_builder = NWBFileBuilder(
                data_path=self.data_path,
                animal_name=self.animal_name,
                date=date,
                nwb_metadata=self.nwb_metadata,
                output_file=self.output_path + self.animal_name + date + ".nwb",
                process_mda=self.extract_mda,
                process_dio=self.extract_dio,
                process_analog=self.extract_analog
            )
            content = nwb_builder.build()
            nwb_builder.write(content)

    def cleanup(self):
        """remove all temporary files structure from preprocessing folder"""

        preprocessing = self.data_path + '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)

    def __is_rec_config_valid(self):
        """ Check if XML is valid with XSD file """

        xml_file_path = ''
        for i in range(len(self.analog_export_args)):
            if self.analog_export_args[i] == '-reconfig':
                xml_file_path = self.analog_export_args[i+1]
        xsd_file_path = str(path) + '/../../fl/data/reconfig_header.xsd'
        xsd_schema = xmlschema.XMLSchema(xsd_file_path)
        return xsd_schema.is_valid(xml_file_path)

