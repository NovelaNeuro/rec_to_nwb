from pynwb import ProcessingModule


class ProcessingModuleCreator:

    @staticmethod
    def create_processing_module(name, description):
        return ProcessingModule(name, description)

