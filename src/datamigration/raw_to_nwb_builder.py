import os
import shutil
from pathlib import Path

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()


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
            parallel_instances=4
    ):
        self.extract_analog = extract_analog
        self.extract_spikes = extract_spikes
        self.extract_dio = extract_dio
        self.extract_lfps = extract_lfps
        self.extract_mda = extract_mda
        self.extract_time = extract_time
        self.animal_name = animal_name
        self.data_path = data_path
        self.dates = dates
        self.metadata = nwb_metadata.metadata
        self.output_path = output_path
        self.probes = nwb_metadata.probes
        self.nwb_metadata = nwb_metadata
        self.parallel_instances = parallel_instances

    def __preprocess_data(self):
        """prepare structre of binary files needed for the future processing"""
        extract_trodes_rec_file(self.data_path,
                                self.animal_name,
                                parallel_instances=self.parallel_instances,
                                extract_analog=self.extract_analog,
                                extract_dio=self.extract_dio,
                                extract_time=self.extract_time,
                                extract_mda=self.extract_mda,
                                extract_lfps=self.extract_lfps,
                                extract_spikes=self.extract_spikes, )

    def build_nwb(self):
        """for each experiment date specified in __init__, colect data about experiment from file-system structure ,
        and write it to NWB file format"""
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
        """remove all temporary structures and files retrived while processing data"""
        preprocessing = self.data_path + '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)
