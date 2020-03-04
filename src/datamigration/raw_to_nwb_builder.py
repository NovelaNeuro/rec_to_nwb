import os
import shutil
from pathlib import Path

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()

_DEFAULT_LFP_EXPORT_ARGS = ('-highpass', '0', '-lowpass', '400',
                            '-interp', '0', '-userefs', '0',
                            '-outputrate', '1500')
_DEFAULT_MDA_EXPORT_ARGS = ('-usespikefilters', '0',
                            '-interp', '500', '-userefs', '1')

class RawToNWBBuilder:

    def __init__(
            self,
            data_path,
            animal_name,
            dates,
            nwb_metadata,
            output_path='',
            extract_analog=False,
            extract_spikes=False,
            extract_lfps=False,
            extract_dio=True,
            extract_time=True,
            extract_mda=True,
            lfp_export_args=_DEFAULT_LFP_EXPORT_ARGS,
            mda_export_args=_DEFAULT_MDA_EXPORT_ARGS,
            parallel_instances=4
    ):
        self.extract_analog = extract_analog
        self.extract_spikes = extract_spikes
        self.extract_dio = extract_dio
        self.extract_lfps = extract_lfps
        self.extract_mda = extract_mda
        self.extract_time = extract_time
        self.lfp_export_args = lfp_export_args
        self.mda_export_args = mda_export_args
        self.animal_name = animal_name
        self.data_path = data_path
        self.dates = dates
        self.metadata = nwb_metadata.metadata
        self.output_path = output_path
        self.probes = nwb_metadata.probes
        self.nwb_metadata = nwb_metadata
        self.parallel_instances = parallel_instances

    def __preprocess_data(self):
        """process data with rec_to_binaries library"""

        extract_trodes_rec_file(self.data_path,
                                self.animal_name,
                                parallel_instances=self.parallel_instances,
                                extract_analog=self.extract_analog,
                                extract_dio=self.extract_dio,
                                extract_time=self.extract_time,
                                extract_mda=self.extract_mda,
                                extract_lfps=self.extract_lfps,
                                extract_spikes=self.extract_spikes,
                                lfp_export_args=self.lfp_export_args,
                                mda_export_args=self.mda_export_args
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
                process_dio=self.extract_dio
            )
            content = nwb_builder.build()
            nwb_builder.write(content)

    def cleanup(self):
        """remove all temporary files structure from preprocessing folder"""

        preprocessing = self.data_path + '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)
