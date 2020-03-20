import logging
import os
import shutil

from rec_to_binaries import extract_trodes_rec_file
import xmlschema

from fl.datamigration.nwb_file_builder import NWBFileBuilder

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

