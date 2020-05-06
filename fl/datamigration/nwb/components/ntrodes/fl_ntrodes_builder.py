from fl.datamigration.nwb.components.ntrodes.fl_ntrodes import FlNTrodes

from fl.datamigration.nwb.components.ntrodes.fl_ntrodes_extractor import FlNTrodesExtractor


class FlNTrodesBuilder:

    def __init__(self, metadata):
        self.metadata = metadata

        self.fl_ntrodes_extractor = FlNTrodesExtractor()

    def build(self, nwb_content):
        return [FlNTrodes(
            metadata=ntrode_metadata,
            device=self.fl_ntrodes_extractor.extract_device(ntrode_metadata, nwb_content),
            map_list=self.fl_ntrodes_extractor.extract_map(ntrode_metadata)
        ) for ntrode_metadata in self.metadata['ntrode probe channel map']]
