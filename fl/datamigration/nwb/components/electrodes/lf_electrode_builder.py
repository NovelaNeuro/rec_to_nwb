from fl.datamigration.nwb.components.electrodes.fl_electrodes import LfElectrode


class LfElectrodesBuilder:

    def build(self, electrode_group):
        return LfElectrode(electrode_group)