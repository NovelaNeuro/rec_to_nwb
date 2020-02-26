from src.datamigration.nwb.components.ntrodes.lf_ntrodes import LfNTrodes

from src.datamigration.nwb.components.ntrodes.ntrodes_extractor import NTrodesExtractor


class LfNTrodesBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

        self.ntrodes_extractor = NTrodesExtractor()

    def build(self, nwb_content):
        return [LfNTrodes(
            metadata=ntrode_metadata,
            device=self.ntrodes_extractor.extract_device(ntrode_metadata, nwb_content),
            map_list=self.ntrodes_extractor.extract_map(ntrode_metadata)
        ) for ntrode_metadata in self.metadata['ntrode probe channel map']]
