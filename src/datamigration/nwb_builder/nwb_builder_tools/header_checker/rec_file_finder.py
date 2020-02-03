from pathlib import Path


class RecFileFinder:

    def __init__(self):
        pass

    @staticmethod
    def find_rec_files(path):
        rec_files = []
        for file_path in Path(path).glob('**/*.rec'):
            rec_files.appe
