from fldatamigration.processing.tools.beartype.beartype import beartype


class FlAssociatedFilesExtractor:

    @beartype
    def __init__(self, files: list):
        self.files = files

    def extract(self):
        content_of_files = []
        for file in self.files:
            with open(file, 'r') as open_file:
                content_of_files.append(open_file.read())
        return content_of_files
