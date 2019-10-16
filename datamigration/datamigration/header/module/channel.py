class Channel:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.id = self.tree.get('id')
        self.bit = self.tree.get('bit')
        self.data_type = self.tree.get('dataType')
        self.start_byte = self.tree.get('startByte')
        self.input = self.tree.get('input')