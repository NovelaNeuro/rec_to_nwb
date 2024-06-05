class CameraSampleFrameCountsInjector:

    @staticmethod
    def inject(timeseries, processing_module_name, nwb_content):
        """Insert timeseries series to nwb file"""
        nwb_content.processing[processing_module_name].add(timeseries)
