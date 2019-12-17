from pathlib import Path


class RecFileFinder:

    def __init__(self):
        self.rec_files = []

    def find_rec_files(self, path):
        for file_path in Path(path).glob('**/*.rec'):
            self.rec_files.append(file_path)
        return self.rec_files
