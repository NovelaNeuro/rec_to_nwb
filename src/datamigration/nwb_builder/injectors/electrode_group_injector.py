class ElectrodeGroupInjector:

    def __init__(self, nwb_content):
        self.nwb_content = nwb_content


    def join_electrode_group(self, electrode_group):
        self.nwb_content.add_electrode_group(electrode_group)