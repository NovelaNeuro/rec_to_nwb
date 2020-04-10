class FlNTrodesExtractor:

    @staticmethod
    def extract_device(ntrode_metadata, nwb_content):
        electrode_group_id = str(ntrode_metadata["electrode_group_id"])
        return nwb_content.devices[electrode_group_id]

    @staticmethod
    def extract_map(ntrode_metadata):
        map_list = []
        for map_element in ntrode_metadata['map'].keys():
            map_list.append((map_element, ntrode_metadata['map'][map_element]))
        return map_list