class ProcessingModuleManager:
    def __init__(self, processing_module):
        self.processing_module = processing_module

    def add_data(self, data):
        self.processing_module.add_data_interface(data)