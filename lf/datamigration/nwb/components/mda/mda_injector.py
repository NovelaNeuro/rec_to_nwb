class MdaInjector:

    @staticmethod
    def inject_mda(electrical_series, nwb_content):
        """insert electrical series to nwb file"""

        nwb_content.add_acquisition(electrical_series)
