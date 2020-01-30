class MdaInjector:

    @staticmethod
    def inject_mda(mda, nwb_content):
        nwb_content.add_acquisition(mda)
