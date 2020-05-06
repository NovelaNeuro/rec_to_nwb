from fldatamigration.processing.nwb.components.device.shanks.fl_shank_builder import FlShankBuilder
from fldatamigration.processing.tools.filter_probe_by_type import filter_probe_by_type
from fldatamigration.processing.tools.validate_parameters import validate_parameters_not_none


class FlShankManager:

    def __init__(self, probes_metadata, electrode_groups_metadata):
        validate_parameters_not_none(__name__, probes_metadata, electrode_groups_metadata)

        self.probes_metadata = probes_metadata
        self.electrode_groups_metadata = electrode_groups_metadata

        self.fl_shank_builder = FlShankBuilder()

    def get_fl_shanks_dict(self, shanks_electrodes_dict):
        validate_parameters_not_none(__name__, shanks_electrodes_dict)

        fl_shanks_dict = {}
        probes_types = []
        for electrode_group_metadata in self.electrode_groups_metadata:
            if electrode_group_metadata['device_type'] not in probes_types:
                fl_shanks = []
                probes_types.append(electrode_group_metadata['device_type'])
                probe_metadata = filter_probe_by_type(self.probes_metadata, electrode_group_metadata['device_type'])

                fl_shanks.extend(self.__build_fl_shanks(
                    probe_metadata=probe_metadata,
                    shanks_electrodes=shanks_electrodes_dict[electrode_group_metadata['device_type']]
                ))
                fl_shanks_dict[electrode_group_metadata['device_type']] = fl_shanks
        return fl_shanks_dict

    def __build_fl_shanks(self, probe_metadata, shanks_electrodes):

        for shank in probe_metadata['shanks']:
            shanks_electrodes_in_shank = []
            for _ in shank['electrodes']:
                shanks_electrodes_in_shank.append(shanks_electrodes.pop(0))
            yield self.__build_single_fl_shank(shank['shank_id'], shanks_electrodes_in_shank)

    def __build_single_fl_shank(self, shank_id, shanks_electrodes):
        return self.fl_shank_builder.build(shank_id, shanks_electrodes)