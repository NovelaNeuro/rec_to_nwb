class ElectrodesCreator:

    def __init__(self):
        self.electrodes_id = -1

    def create_electrode(self, nwb_content, electrode_group):
        self.electrodes_id += 1

        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=electrode_group,
            id=self.electrodes_id
        )
