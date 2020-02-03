import logging.config
import os

from src.datamigration.extension.ntrode import NTrode

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class NTrodesCreator:

    @staticmethod
    def create_ntrode(metadata, device, map_list):
        return NTrode(
            probe_id=metadata["probe_id"],
            ntrode_id=metadata['ntrode_id'],
            device=device,
            location='-',
            description='-',
            name='ntrode ' + str(metadata['ntrode_id']),
            map=map_list
        )