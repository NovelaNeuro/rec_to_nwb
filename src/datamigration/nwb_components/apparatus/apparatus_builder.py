from src.datamigration.nwb_components.apparatus.apparatus_creator import ApparatusCreator
from src.datamigration.nwb_components.apparatus.apparatus_extractor import ApparatusExtractor


class ApparatusBuilder:

    def __init__(self, apparatus_metadata):
        self.apparatus_extractor = ApparatusExtractor(apparatus_metadata)
        self.apparatus_creator = ApparatusCreator()

    def build(self):
        edges, nodes = self.apparatus_extractor.get_data()
        return self.apparatus_creator.create_apparatus(edges, nodes)
