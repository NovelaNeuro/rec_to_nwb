import os

path = os.path.dirname(os.path.abspath(__file__))


class FlAssociatedFilesReader:

    @staticmethod
    def read(file_path):
        with open(str(path) + '/../../../../../' + file_path, 'r') as open_file:
            return open_file.read()
