import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SpikeChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.hw_chan = self.tree.get('hwChan')
        self.max_disp = self.tree.get('maxDisp')
        self.thresh = self.tree.get('thresh')
        self.trigger_on = self.tree.get('triggerOn')