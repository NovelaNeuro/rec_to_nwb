from rec_to_nwb.processing.nwb.components.electrodes.extension.fl_electrode_extension import FlElectrodeExtension
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlElectrodeExtensionBuilder:

    @staticmethod
    @beartype
    def build(rel_x: list, rel_y: list, rel_z: list, hw_chan: list, ntrode_id: list, channel_id: list,
              bad_channels: list, probe_shank: list, probe_electrode: list, ref_elect_id: list
              ) -> FlElectrodeExtension:
        return FlElectrodeExtension(
            rel_x=rel_x,
            rel_y=rel_y,
            rel_z=rel_z,
            hw_chan=hw_chan,
            ntrode_id=ntrode_id,
            channel_id=channel_id,
            bad_channels=bad_channels,
            probe_shank=probe_shank,
            probe_electrode=probe_electrode,
            ref_elect_id=ref_elect_id
        )
