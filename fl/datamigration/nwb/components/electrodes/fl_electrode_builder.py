from pynwb.ecephys import ElectrodeGroup

from fl.datamigration.nwb.components.electrodes.fl_electrodes import FlElectrode
from fl.datamigration.tools.beartype.beartype import beartype


class FlElectrodesBuilder:

    @staticmethod
    @beartype
    def build(electrode_id: int, electrode_group: ElectrodeGroup):
        return FlElectrode(electrode_id, electrode_group)