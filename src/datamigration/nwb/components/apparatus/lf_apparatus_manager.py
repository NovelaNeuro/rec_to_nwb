from src.datamigration.nwb.components.apparatus.lf_apparatus_builder import LfApparatusBuilder
from src.datamigration.nwb.components.apparatus.lf_apparatus_extractor import LfApparatusExtractor


class LfApparatusManager:

    def __init__(self, apparatus_metadata):
        self.lf_apparatus_extractor = LfApparatusExtractor(apparatus_metadata)

    def get_lf_apparatus(self):
        edges, nodes = self.lf_apparatus_extractor.get_data()
        return LfApparatusBuilder.build(edges, nodes)
