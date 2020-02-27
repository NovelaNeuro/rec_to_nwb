from src.datamigration.nwb.components.electrodes.lf_electrodes import LfElectrode


class LfElectrodesBuilder:

    def build(self, electrode_group):
        return LfElectrode(electrode_group)