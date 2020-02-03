import logging.config
import os

import defusedxml.cElementTree as ET

from src.datamigration.header.module.configuration import Configuration

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Header:

    def __init__(self, filename):
        self.tree = ET.parse(filename)
        self.configuration = Configuration(self.tree.getroot())
