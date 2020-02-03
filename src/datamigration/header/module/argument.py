import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class Argument:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.flag = self.tree.get('flag')
        self.value = self.tree.get('value')