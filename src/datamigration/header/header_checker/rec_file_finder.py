from pathlib import Path


class RecFileFinder:

    @staticmethod
    def find_rec_files(path):
        rec_files = []
        for file_path in Path(path).glob('**/*.rec'):
            rec_files.append(file_path)
        return rec_files
