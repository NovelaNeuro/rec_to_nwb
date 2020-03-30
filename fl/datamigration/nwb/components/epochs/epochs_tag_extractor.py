class EpochsTagExtractor:

    def __init__(self, datasets):
        self.datasets = datasets

    def get_tags(self):
        return [dataset.name for dataset in self.datasets]