from lf.datamigration.tools.validate_input_parameters import validate_input_parameters


class ElectrodesCreator:

    def __init__(self):
        self.electrode_id = -1

    def create(self, nwb_content, lf_electrode):
        self.__validate_parameters(lf_electrode, nwb_content)
        self.electrode_id += 1

        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=lf_electrode.electrode_group,
            id=self.electrode_id
        )

    @staticmethod
    def __validate_parameters(lf_electrode, nwb_content):
        validate_input_parameters(__name__, nwb_content, lf_electrode)
        validate_input_parameters(__name__, lf_electrode.electrode_group)
