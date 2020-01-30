from pynwb import ProcessingModule


class ProcessingModuleCreator:

    def __init__(self, name, description):
        self.processing_module = ProcessingModule(name, description)

    def add_data(self, data):
        self.processing_module.add_data_interface(data)
