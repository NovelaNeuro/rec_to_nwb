from src.datamigration.nwb_components.apparatus.apparatus_creator import ApparatusCreator
from src.datamigration.nwb_components.apparatus.apparatus_extractor import ApparatusExtractor


class ApparatusBuilder:

    def __init__(self, apparatus_metadata):
        self.apparatus_extractor = ApparatusExtractor(apparatus_metadata)

    def build(self):
        edges, nodes = self.apparatus_extractor.get_data()
        return ApparatusCreator.create_apparatus(edges, nodes)
