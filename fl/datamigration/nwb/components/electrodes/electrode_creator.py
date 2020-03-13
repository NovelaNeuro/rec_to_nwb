from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodesCreator:

    def __init__(self):
        self.electrode_id = -1

    def create(self, nwb_content, fl_electrode):
        self.__validate_parameters(fl_electrode, nwb_content)
        self.electrode_id += 1

        nwb_content.add_electrode(
            x=0.0,
            y=0.0,
            z=0.0,
            imp=0.0,
            location='None',
            filtering='None',
            group=fl_electrode.electrode_group,
            id=self.electrode_id
        )

    @staticmethod
    def __validate_parameters(fl_electrode, nwb_content):
        validate_parameters_not_none(__name__, nwb_content, fl_electrode)
        validate_parameters_not_none(__name__, fl_electrode.electrode_group)
