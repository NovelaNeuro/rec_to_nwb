from pynwb.device import Device

from rec_to_nwb.processing.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlNwbElectrodeGroupBuilder:

    @staticmethod
    @beartype
    def build(metadata: dict, device: Device):
        return FlNwbElectrodeGroup(
            name=str(metadata["id"]),
            description=metadata['description'],
            location=metadata['location'],
            device=device,
            targeted_location=metadata['targeted_location'],
            targeted_x=float(metadata['targeted_x']),
            targeted_y=float(metadata['targeted_y']),
            targeted_z=float(metadata['targeted_z']),
            units=metadata['units'],
        )
