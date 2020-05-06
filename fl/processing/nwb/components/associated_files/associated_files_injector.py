class AssociatedFilesInjector:
    """"Inject associated_files object inside NWBFile"."""

    @classmethod
    def inject(cls, associated_files, processing_module_name, nwb_content):
        """insert associated_files extension to specified processing module in nwb file"""

        nwb_content.processing[processing_module_name].add(associated_files)
