import os

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder


class RawToNWBBuilder:

    def __init__(self, data_path, animal_name, date, dataset, metadata_path, output_path):
        self.animal_name = animal_name
        self.data_path = data_path

        self.nwbBuilder = NWBFileBuilder(
            data_path=data_path,
            animal_name=animal_name,
            date=date,
            dataset=dataset,
            metadata_path=metadata_path,
            output_file=output_path
        )

    def __preprocess_data(self):
        extract_trodes_rec_file(self.data_path, self.animal_name, parallel_instances=4)

    def build_nwb(self):
        self.__preprocess_data()
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)

    def cleanup(self):
        os.remove('header.xml')
        os.rmdir('preprocessing')
