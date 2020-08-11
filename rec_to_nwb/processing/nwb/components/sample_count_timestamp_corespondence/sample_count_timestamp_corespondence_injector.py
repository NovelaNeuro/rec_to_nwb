class SampleCountTimestampCorespondenceInjector:

    @staticmethod
    def inject(timeseries, nwb_content):
        """insert timeseries series to nwb file"""

        nwb_content.add_acquisition(timeseries)
