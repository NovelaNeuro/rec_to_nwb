from pynwb.ecephys import ElectrodeGroup
from rec_to_nwb.processing.nwb.components.electrodes.fl_electrodes import \
    FlElectrode
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlElectrodesBuilder:

    @staticmethod
    @beartype
    def build(electrode_id: int, electrode_group: ElectrodeGroup):
        return FlElectrode(electrode_id, electrode_group)
