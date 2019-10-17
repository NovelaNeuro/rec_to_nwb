class SpikeChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.hw_chan = self.tree.get('hwChan')
        self.max_disp = self.tree.get('maxDisp')
        self.thresh = self.tree.get('thresh')
        self.trigger_on = self.tree.get('triggerOn')