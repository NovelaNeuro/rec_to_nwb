from rec_to_nwb.processing.nwb.components.analog.analog_creator import AnalogCreator
from rec_to_nwb.processing.nwb.components.analog.analog_files import AnalogFiles
from rec_to_nwb.processing.nwb.components.analog.analog_injector import AnalogInjector
from rec_to_nwb.processing.nwb.components.analog.fl_analog_manager import FlAnalogManager


class AnalogOriginator:

    def __init__(self, datasets, metadata):
        self.datasets = datasets
        self.metadata = metadata
        self.continuous_time_files = self.__get_continuous_time_files()

    def make(self, nwb_content):
        analog_directories = [single_dataset.get_data_path_from_dataset('analog') for single_dataset in self.datasets]
        analog_files = AnalogFiles(analog_directories)
        analog_manager = FlAnalogManager(
            analog_files=analog_files.get_files(),
            continuous_time_files=self.continuous_time_files
        )
        fl_analog = analog_manager.get_analog()
        analog_injector = AnalogInjector(nwb_content)
        analog_injector.inject(AnalogCreator.create(fl_analog, self.metadata['units']['analog']), 'behavior')

    def __get_continuous_time_files(self):
        return [single_dataset.get_continuous_time() for single_dataset in self.datasets]
