class StreamDisplay:

    def __init__(self, element):
        self.tree = element
        self.tag = self.tree.tag
        self.background_color = self.tree.get('backgroundColor')
        self.columns = self.tree.get('columns')
        self.pages = self.tree.get('pages')