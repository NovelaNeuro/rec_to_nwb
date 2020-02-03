import logging.config
import os

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class StreamDisplay:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.background_color = self.tree.get('backgroundColor')
        self.columns = self.tree.get('columns')
        self.pages = self.tree.get('pages')