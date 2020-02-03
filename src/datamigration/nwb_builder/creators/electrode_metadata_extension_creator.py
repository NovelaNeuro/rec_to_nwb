import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class ElectrodesMetadataExtensionCreator:
    def __init__(self):
        self.rel_x = []
        self.rel_y = []
        self.rel_z = []

    def create_extensions(self, electrode):
        self.rel_x.append(electrode['rel_x'])
        self.rel_y.append(electrode['rel_y'])
        self.rel_z.append(electrode['rel_z'])
