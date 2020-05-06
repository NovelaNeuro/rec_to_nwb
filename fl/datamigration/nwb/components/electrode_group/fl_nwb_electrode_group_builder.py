from pynwb.device import Device

from fl.datamigration.nwb.components.electrode_group.fl_nwb_electrode_group import FlNwbElectrodeGroup
from fl.datamigration.tools.beartype.beartype import beartype


class FlNwbElectrodeGroupBuilder:

    @staticmethod
    @beartype
    def build(metadata: dict, device: Device):
        return FlNwbElectrodeGroup(
            name='electrode group ' + str(metadata["id"]),
            description=metadata['description'],
            location=metadata['location'],
            device=device,
            targeted_location=metadata['targeted_location'],
            targeted_x=metadata['targeted_x'],
            targeted_y=metadata['targeted_y'],
            targeted_z=metadata['targeted_z'],
            units=metadata['units'],
        )
