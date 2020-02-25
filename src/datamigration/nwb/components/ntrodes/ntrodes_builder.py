from src.datamigration.nwb.components.ntrodes.ntrodes_creator import NTrodesCreator
from src.datamigration.nwb.components.ntrodes.ntrodes_extractor import NTrodesExtractor
from src.datamigration.nwb.components.ntrodes.ntrodes_injector import NTrodesInjector


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
