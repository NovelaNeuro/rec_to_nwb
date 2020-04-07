class Argument:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.flag = self.tree.get('flag')
        self.value = self.tree.get('value')