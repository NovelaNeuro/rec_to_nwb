class AssociatedFilesInjector:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content

    def inject(self, associated_files, processing_module_name):
        """insert associated_files extension to specified processing module in nwb file"""

        self.nwb_content.processing[processing_module_name].add(associated_files)
