import os


class AnalogFiles:

    def __init__(self, directories):
        self.directories = directories

    def get_files(self):
        return [self.__get_dict(dataset) for dataset in self.directories]

    @classmethod
    def __get_dict(cls, directory):
        analog_dict = {}
        files = os.listdir(directory)
        files.sort()
        for file in files:
            if file.endswith('.dat'):
                split_filename = file.split('.')
                analog_dict[split_filename[-2].split('_')[-1]] = directory + '/' + file
        return analog_dict
