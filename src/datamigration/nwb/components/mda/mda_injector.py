class MdaInjector:

    @staticmethod
    def inject_mda(electrical_series, nwb_content):
        nwb_content.add_acquisition(electrical_series)
