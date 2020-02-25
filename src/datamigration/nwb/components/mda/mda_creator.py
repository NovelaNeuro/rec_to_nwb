from pynwb import ecephys


class MdaCreator:

    @classmethod
    def create_mda(cls, lf_mda):
        return ecephys.ElectricalSeries(
            name="e-series",
            data=lf_mda.mda_data.mda_data,
            electrodes=lf_mda.electrode_table_region,
            timestamps=lf_mda.mda_data.mda_timestamps,
            resolution=lf_mda.sampling_rate,
            comments="sample comment",
            description="Electrical series registered on electrode"
        )
