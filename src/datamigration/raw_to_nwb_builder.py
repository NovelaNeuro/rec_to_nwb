import os
import shutil

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder


class RawToNWBBuilder:

    def __init__(self, data_path, animal_name, date, dataset, metadata_path, output_path):
        self.animal_name = animal_name
        self.data_path = data_path
        self.date = date
        self.dataset = dataset
        self.metadata_path = metadata_path
        self.output_path = output_path

    def __preprocess_data(self):
        extract_trodes_rec_file(self.data_path, self.animal_name, parallel_instances=4)

    def build_nwb(self):
        self.__preprocess_data()
        self.nwbBuilder = NWBFileBuilder(
            data_path=self.data_path,
            animal_name=self.animal_name,
            date=self.date,
            dataset=self.dataset,
            metadata_path=self.metadata_path,
            output_file=self.output_path
        )
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)

    def cleanup(self):
        preprocessing = self.data_path + '/' + self.animal_name + '/preprocessing'
        if os.path.exists(preprocessing):
            shutil.rmtree(preprocessing)
