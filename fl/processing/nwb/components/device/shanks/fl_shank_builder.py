from fl.processing.nwb.components.device.shanks.fl_shank import FlShank


class FlShankBuilder:

    @staticmethod
    def build(shank_id, shanks_electrodes):
        return FlShank(
            shank_id=shank_id,
            shanks_electrodes=shanks_electrodes
        )