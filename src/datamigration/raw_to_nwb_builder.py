import os
import shutil
from pathlib import Path

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder

path = Path(__file__).parent.parent
path.resolve()


class RawToNWBBuilder:

    def __init__(self, data_path, animal_name, date, nwb_metadata, output_path):
        self.animal_name = animal_name
        self.data_path = data_path
        self.date = date
        self.metadata = nwb_metadata.metadata
        self.output_path = output_path
        self.probes = nwb_metadata.probes
        self.nwb_metadata = nwb_metadata

    def __preprocess_data(self):
        extract_trodes_rec_file(self.data_path, self.animal_name, parallel_instances=4)

    def build_nwb(self):
        self.__preprocess_data()
        self.nwbBuilder = NWBFileBuilder(
            data_path=self.data_path,
            animal_name=self.animal_name,
            date=self.date,
            nwb_metadata=self.nwb_metadata,
            output_file=self.output_path
            )
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)
        return content

    def cleanup(self):
        preprocessing = self.data_path + '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)
