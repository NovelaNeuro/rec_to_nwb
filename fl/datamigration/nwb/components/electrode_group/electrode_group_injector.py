from fl.datamigration.tools.name_extractor import NameExtractor
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodeGroupInjector:

    def inject_all_electrode_groups(self, nwb_content, electrode_groups):
        """insert electrode groups to nwb file"""

        validate_parameters_not_none(
            class_name=__name__,
            args=[nwb_content, electrode_groups],
            args_name=[NameExtractor.extract_name(self.inject_all_electrode_groups)[1],
                       NameExtractor.extract_name(self.inject_all_electrode_groups)[2]]
        )
        for electrode_group in electrode_groups:
            self.__inject_electrode_group(nwb_content, electrode_group)

    @staticmethod
    def __inject_electrode_group(nwb_content, electrode_group):
        nwb_content.add_electrode_group(electrode_group)
