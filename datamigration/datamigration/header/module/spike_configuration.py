from .spike_n_trode import SpikeNTrode


class SpikeConfiguration:

    def __init__(self, element):
        self.tree = element
        self.spike_n_trodes = [SpikeNTrode(spike_n_trode_element) for spike_n_trode_element
                               in self.tree.findall('SpikeNTrode')]
        self.tag = self.tree.tag
        self.categories = self.tree.get('categories')

