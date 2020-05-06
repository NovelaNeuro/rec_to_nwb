from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_factory import \
    FlElectrodeExtensionFactory
from fl.datamigration.tools.beartype.beartype import beartype
from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class FlElectrodeExtensionBuilder:

    @staticmethod
    @beartype
    def build(rel_x: list, rel_y: list, rel_z: list, hw_chan: list, ntrode_id: list, bad_channels: list,
              probe_shank: list, probe_channel: list):
        return FlElectrodeExtension(
            rel_x=rel_x,
            rel_y=rel_y,
            rel_z=rel_z,
            hw_chan=hw_chan,
            ntrode_id=ntrode_id,
            bad_channels=bad_channels,
            probe_shank=probe_shank,
            probe_channel=probe_channel
        )
