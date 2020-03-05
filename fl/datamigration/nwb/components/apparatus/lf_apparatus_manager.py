from fl.datamigration.nwb.components.apparatus.fl_apparatus_builder import LfApparatusBuilder
from fl.datamigration.nwb.components.apparatus.fl_apparatus_extractor import LfApparatusExtractor


class LfApparatusManager:

    def __init__(self, apparatus_metadata):
        self.fl_apparatus_extractor = LfApparatusExtractor(apparatus_metadata)

    def get_fl_apparatus(self):
        """extract apparatus from metadata.yml file and build LfApparatus"""

        edges, nodes = self.fl_apparatus_extractor.get_data()
        return LfApparatusBuilder.build(edges, nodes)
