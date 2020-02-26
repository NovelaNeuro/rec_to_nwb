from src.datamigration.nwb.components.apparatus.apparatus_lf_builder import ApparatusLfBuilder
from src.datamigration.nwb.components.apparatus.apparatus_extractor import ApparatusExtractor


class ApparatusManager:

    def __init__(self, apparatus_metadata):
        self.apparatus_extractor = ApparatusExtractor(apparatus_metadata)

    def get_lf_apparatus(self):
        edges, nodes = self.apparatus_extractor.get_data()
        return ApparatusLfBuilder.build(edges, nodes)
