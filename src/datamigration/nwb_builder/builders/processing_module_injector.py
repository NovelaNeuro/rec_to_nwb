class ProcessingModuleInjector:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content

    def join_processing_module(self, processing_module):
        self.nwb_content.add_processing_module(processing_module)

