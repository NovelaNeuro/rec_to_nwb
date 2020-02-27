class DioInjector:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content

    def inject(self, behavioral_events, processing_module_name):
        """insert behavioral events to specified processing module in nwb file"""

        self.nwb_content.processing[processing_module_name].add_data_interface(behavioral_events)
