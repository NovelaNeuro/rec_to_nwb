from pynwb.device import Device

from fl.processing.nwb.components.electrode_group.fl_electrode_group import FlElectrodeGroup
from fl.processing.tools.beartype.beartype import beartype


class FlElectrodeGroupBuilder:

    @staticmethod
    @beartype
    def build(metadata: dict, device: Device):
        return FlElectrodeGroup(
            name='electrode group ' + str(metadata["id"]),
            description=metadata['description'],
            location=metadata['location'],
            device=device
        )
