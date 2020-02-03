import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class DispChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.analyze = self.tree.get('analyze')
        self.id = self.tree.get('id')
        self.device = self.tree.get('device')
        self.color = self.tree.get('color')
        self.max_disp = self.tree.get('maxDisp')