from fl.datamigration.tools.name_extractor import NameExtractor
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
        validate_parameters_not_none(
            class_name=__name__,
            args=[nwb_content, fl_electrode],
            args_name=[NameExtractor.extract_name(ElectrodesCreator.__validate_parameters)[1],
                       NameExtractor.extract_name(ElectrodesCreator.__validate_parameters)[0]]
        )
        validate_parameters_not_none(
            class_name=__name__,
            args=[fl_electrode.electrode_group],
            args_name=[NameExtractor.extract_name(fl_electrode.__init__)[1]]
        )
