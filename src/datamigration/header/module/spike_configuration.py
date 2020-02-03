import logging.config
import os

from src.datamigration.header.module.spike_n_trode import SpikeNTrode

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SpikeConfiguration:

    def __init__(self, element):
        self.tree = element
        self.spike_n_trodes = [SpikeNTrode(spike_n_trode_element) for spike_n_trode_element
                               in self.tree.findall('SpikeNTrode')]
        self.tag = self.tree.tag
        self.categories = self.tree.get('categories')

