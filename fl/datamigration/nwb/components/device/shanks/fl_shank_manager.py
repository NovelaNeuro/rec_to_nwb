from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlShankManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        validate_parameters_not_none(__name__, probes_metadata, electrode_groups_metadata)
        #     ToDo for item in probes_metadata not none

        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_shank_builder = FlShankBuilder()

    def get_fl_shanks_dict(self, shanks_electrodes_dict):
        validate_parameters_not_none(__name__, shanks_electrodes_dict)

