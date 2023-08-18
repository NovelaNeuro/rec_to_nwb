import glob
import os


class AnalogFiles:
    def __init__(self, directories):
        self.directories = directories

    def get_files(self):
        return [self.__get_dict(dataset) for dataset in self.directories]

    @classmethod
    def __get_dict(cls, directory):
        analog_dict = {}
        for file in glob.glob(os.path.join(directory, "*.dat")):
            if "timestamps" in file:
                analog_name = "timestamps"
            else:
                analog_name = file.split(".")[-2]
            analog_dict[analog_name] = os.path.join(directory, file)
        return analog_dict
