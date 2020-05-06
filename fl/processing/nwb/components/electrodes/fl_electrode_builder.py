from pynwb.ecephys import ElectrodeGroup

from fl.processing.nwb.components.electrodes.fl_electrodes import FlElectrode
from fl.processing.tools.beartype.beartype import beartype


class FlElectrodesBuilder:

    @staticmethod
    @beartype
    def build(electrode_id: int, electrode_group: ElectrodeGroup):
        return FlElectrode(electrode_id, electrode_group)