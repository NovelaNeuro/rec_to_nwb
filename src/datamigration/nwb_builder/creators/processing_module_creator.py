from pynwb import ProcessingModule


class ProcessingModuleCreator:

    def __init__(self, name, description):
        self.processing_module = ProcessingModule(name, description)

    def insert(self, data):
        try:
            self.processing_module.add_data_interface(data)
        except TypeError as err:
            # log error instead
            print(err)
