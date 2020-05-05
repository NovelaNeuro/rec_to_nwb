class FlAssociatedFilesExtractor:

    def __init__(self, files):
        self.files = files

    def extract(self):
        content_of_files = []
        for file in self.files:
            with open(file, 'r') as open_file:
                content_of_files.append(open_file.read())
        return content_of_files
