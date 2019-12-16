import os

from rec_to_binaries import extract_trodes_rec_file

from src.datamigration.nwb_file_builder import NWBFileBuilder
from src.test.e2etests.experiment_data import ExperimentData


class RawToNWBBuilder:

    def __init__(self, animal_name, date, dataset, metadata_path):
        self.animal_name = animal_name
        self.date = date
        self.dataset = dataset
        self.metadata_path = metadata_path

    def extract_data(self):
        extract_trodes_rec_file(ExperimentData.root_path, self.animal_name, parallel_instances=4)

    def build_nwb(self):
        self.nwbBuilder = NWBFileBuilder(
            data_path=ExperimentData.root_path,
            animal_name=self.animal_name,
            date=self.date,
            dataset=self.dataset,
            xsd_path=ExperimentData.xsd_path,
            config_path=self.metadata_path
        )
        content = self.nwbBuilder.build()
        self.nwbBuilder.write(content)

    def _cleanup(self):
        os.remove('header.xml')
        os.rmdir('preprocessing')
