import logging.config
import os

from src.datamigration.extension.fl_electrode_group import FLElectrodeGroup

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodeGroupBuilder:

    @staticmethod
    def create_electrode_group(metadata, device):
        return FLElectrodeGroup(
            id=metadata['id'],
            device=device,
            location=str(metadata['location']),
            description=str(metadata['description']),
            name='electrode group ' + str(metadata["id"])
        )