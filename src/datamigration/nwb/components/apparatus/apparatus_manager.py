from src.datamigration.nwb.components.apparatus.lf_apparatus_builder import LfApparatusBuilder
from src.datamigration.nwb.components.apparatus.apparatus_extractor import ApparatusExtractor


class ApparatusManager:

    def __init__(self, apparatus_metadata):
        self.apparatus_extractor = ApparatusExtractor(apparatus_metadata)

    def get_lf_apparatus(self):
        edges, nodes = self.apparatus_extractor.get_data()
        return LfApparatusBuilder.build(edges, nodes)
