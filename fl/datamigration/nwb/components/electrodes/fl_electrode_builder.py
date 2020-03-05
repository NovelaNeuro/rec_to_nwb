from fl.datamigration.nwb.components.electrodes.fl_electrodes import FlElectrode


class FlElectrodesBuilder:

    def build(self, electrode_group):
        return FlElectrode(electrode_group)