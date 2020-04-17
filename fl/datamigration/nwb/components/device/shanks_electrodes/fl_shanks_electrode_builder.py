from fl.datamigration.nwb.components.device.shanks_electrodes.fl_shanks_electrode import FlShanksElectrode


class FlShanksElectrodeBuilder:

    @staticmethod
    def build(shank_id, electrode_metadata):
        return FlShanksElectrode(
            shank_id=shank_id,
            shanks_electrode_id=electrode_metadata['id'],
            rel_x=electrode_metadata['rel_x'],
            rel_y=electrode_metadata['rel_y'],
            rel_z=electrode_metadata['rel_z']
        )
