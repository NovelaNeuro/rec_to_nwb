from rec_to_nwb.processing.nwb.components.analog.analog_creator import AnalogCreator
from rec_to_nwb.processing.nwb.components.analog.analog_files import AnalogFiles
from rec_to_nwb.processing.nwb.components.analog.analog_injector import AnalogInjector
from rec_to_nwb.processing.nwb.components.analog.fl_analog_manager import FlAnalogManager


class AnalogOriginator:

    @staticmethod
    def make(nwb_content, datasets, continuous_time_files, metadata):
        analog_directories = [single_dataset.get_data_path_from_dataset('analog') for single_dataset in datasets]
        analog_files = AnalogFiles(analog_directories)
        analog_manager = FlAnalogManager(
            analog_files=analog_files.get_files(),
            continuous_time_files=continuous_time_files()
        )
        fl_analog = analog_manager.get_analog()
        analog_injector = AnalogInjector(nwb_content)
        analog_injector.inject(AnalogCreator.create(fl_analog, metadata['units']['analog']), 'behavior')