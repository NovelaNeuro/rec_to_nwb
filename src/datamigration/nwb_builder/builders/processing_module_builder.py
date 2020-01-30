from src.datamigration.nwb_builder.creators.processing_module_creator import ProcessingModuleCreator
from src.datamigration.nwb_builder.injectors.processing_module_injector import ProcessingModuleInjector


class ProcessingModuleBuilder:
    def __init__(self, nwb_content):
        self.creator = ProcessingModuleCreator()
        self.injector = ProcessingModuleInjector(nwb_content)



    def build(self, name, description):
        processing_module = self.creator.create_processing_module(name, description)
        self.injector.join_processing_module(processing_module)
        return processing_module

