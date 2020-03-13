from fl.datamigration.nwb.components.electrodes.fl_electrode_builder import FlElectrodesBuilder
from fl.datamigration.tools.filter_probe_by_type import filter_probe_by_type
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_electrodes_builder = FlElectrodesBuilder()

    def get_fl_electrodes(self, electrode_groups):
        self.__validate_parameters(electrode_groups)
        fl_electrodes = []

        for counter, electrode_group_metadata in enumerate(self.electrode_groups_metadata):
            probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])

            for shank in probe_metadata['shanks']:
                for _ in shank['electrodes']:
                    fl_electrodes.append(self.fl_electrodes_builder.build(electrode_groups[counter]))

        return fl_electrodes

    def __validate_parameters(self, electrode_groups):
        validate_parameters_not_none(__name__, self.probes_metadata, self.electrode_groups_metadata, electrode_groups)
        [validate_parameters_not_none(__name__, electrode_group.name) for electrode_group in electrode_groups]






