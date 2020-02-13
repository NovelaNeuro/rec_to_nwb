from pynwb import ecephys


class MdaCreator:

    @classmethod
    def create_mda(cls,sampling_rate, electrode_table_region, extracted_mda_data):
        return ecephys.ElectricalSeries(
            name="e-series",
            data=extracted_mda_data.mda_data,
            electrodes=electrode_table_region,
            timestamps=extracted_mda_data.mda_timestamps,
            resolution=sampling_rate,
            comments="sample comment",
            description="Electrical series registered on electrode"
        )
