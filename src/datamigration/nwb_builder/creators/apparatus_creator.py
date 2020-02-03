import logging.config
import os

from src.datamigration.extension.apparatus import Apparatus

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ApparatusCreator:
    @staticmethod
    def create_apparatus(edges, nodes):
        return Apparatus(
            name='apparatus',
            edges=edges,
            nodes=nodes
        )