from fldatamigration.processing.nwb.components.apparatus.fl_apparatus_builder import FlApparatusBuilder
from fldatamigration.processing.nwb.components.apparatus.fl_apparatus_extractor import FlApparatusExtractor


class FlApparatusManager:

    def __init__(self, apparatus_metadata):
        self.fl_apparatus_extractor = FlApparatusExtractor(apparatus_metadata)

    def get_fl_apparatus(self):
        """extract apparatus from metadata.yml file and build FlApparatus"""

        edges, nodes = self.fl_apparatus_extractor.get_data()
        return FlApparatusBuilder.build(edges, nodes)
