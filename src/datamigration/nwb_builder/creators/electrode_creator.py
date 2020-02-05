class ElectrodesCreator:


    def create_electrode_from_probe(self):


    @staticmethod
    def create_electrode(nwb_content, electrode_group, electrodes_counter):
        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=electrode_group,
            id=electrodes_counter
        )