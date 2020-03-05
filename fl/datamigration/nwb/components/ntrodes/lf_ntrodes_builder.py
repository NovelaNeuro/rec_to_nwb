from fl.datamigration.nwb.components.ntrodes.fl_ntrodes import LfNTrodes

from fl.datamigration.nwb.components.ntrodes.fl_ntrodes_extractor import LfNTrodesExtractor


class LfNTrodesBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

        self.fl_ntrodes_extractor = LfNTrodesExtractor()

    def build(self, nwb_content):
        return [LfNTrodes(
            metadata=ntrode_metadata,
            device=self.fl_ntrodes_extractor.extract_device(ntrode_metadata, nwb_content),
            map_list=self.fl_ntrodes_extractor.extract_map(ntrode_metadata)
        ) for ntrode_metadata in self.metadata['ntrode probe channel map']]
