class DispChannel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.analyze = self.tree.get('analyze')
        self.id = self.tree.get('id')
        self.device = self.tree.get('device')
        self.color = self.tree.get('color')
        self.max_disp = self.tree.get('maxDisp')