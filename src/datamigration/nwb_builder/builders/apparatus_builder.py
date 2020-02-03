import logging.config
import os

from src.datamigration.nwb_builder.creators.apparatus_creator import ApparatusCreator
from src.datamigration.nwb_builder.extractors.apparatus_extractor import ApparatusExtractor

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ApparatusBuilder:

    def __init__(self, metadata):
        self.metadata = metadata
        self.apparatus_extractor = ApparatusExtractor(metadata)
        self.apparatus_creator = ApparatusCreator()

    def build(self):
        edges, nodes = self.apparatus_extractor.get_data()
        return self.apparatus_creator.create_apparatus(edges, nodes)
