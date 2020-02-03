import logging.config
import os

from src.datamigration.header.module.spike_channel import SpikeChannel

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


class SpikeNTrode:

    def __init__(self, element):
        self.tree = element
        self.spike_channels = [SpikeChannel(spike_channel_element) for spike_channel_element
                               in self.tree.findall('SpikeChannel')]
        self.tag = self.tree.tag
        self.low_filter = self.tree.get('lowFilter')
        self.lfp_chan = self.tree.get('LFPChan')
        self.lfp_filter_on = self.tree.get('lfpFilterOn')
        self.ref_group = self.tree.get('refGroup')
        self.group_ref_on = self.tree.get('groupRefOn')
        self.lfp_high_filter = self.tree.get('LFPHighFilter')
        self.hight_filter = self.tree.get('highFilter')
        self.color = self.tree.get('color')
        self.ref_chan = self.tree.get('refChan')
        self.id = self.tree.get('id')
        self.lfp_ref_on = self.tree.get('lfpRefOn')
        self.filter_on = self.tree.get('filterOn')
        self.ref_on = self.tree.get('refOn')
        self.module_data_on = self.tree.get('moduleDataOn')
        self.ref_n_trode_id = self.tree.get('refNTrodeID')
