class SampleCountTimestampCorespondenceInjector:

    @staticmethod
    def inject(timeseries, processing_module_name, nwb_content):
        """insert timeseries series to nwb file"""
        nwb_content.processing[processing_module_name].add(timeseries)

