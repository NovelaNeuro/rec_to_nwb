import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodesExtractor:

    @staticmethod
    def extract_device(ntrode_metadata, nwb_content):
        probe_id = str(ntrode_metadata["probe_id"])
        return nwb_content.devices[probe_id]

    @staticmethod
    def extract_map(ntrode_metadata):
        map_list = []
        for map_element in ntrode_metadata['map'].keys():
            map_list.append((map_element, ntrode_metadata['map'][map_element]))
        return map_list