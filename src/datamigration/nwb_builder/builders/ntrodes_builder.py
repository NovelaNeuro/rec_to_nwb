import logging.config
import os

from src.datamigration.nwb_builder.creators.ntrodes_creator import NTrodesCreator
from src.datamigration.nwb_builder.extractors.ntrodes_extractor import NTrodesExtractor
from src.datamigration.nwb_builder.injectors.ntrodes_injector import NTrodesInjector

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodesBuilder:
    def __init__(self, metadata):
        self.metadata = metadata
        self.ntrodes_extractor = NTrodesExtractor()
        self.ntrodes_creator = NTrodesCreator()
        self.ntrodes_injector = NTrodesInjector()

    def build(self, nwb_content):
        for ntrode_metadata in self.metadata['ntrode probe channel map']:
            device = self.ntrodes_extractor.extract_device(ntrode_metadata, nwb_content)
            map_list = self.ntrodes_extractor.extract_map(ntrode_metadata)

            ntrode = self.ntrodes_creator.create_ntrode(ntrode_metadata, device, map_list)
            self.ntrodes_injector.inject_ntrode(nwb_content, ntrode)
