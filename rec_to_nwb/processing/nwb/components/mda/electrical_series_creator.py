from pynwb import ecephys


class ElectricalSeriesCreator:

    @classmethod
    def create_mda(cls, fl_mda):
        return ecephys.ElectricalSeries(
            name="e-series",
            data=fl_mda.mda_data.mda_data,
            electrodes=fl_mda.electrode_table_region,
            timestamps=fl_mda.mda_data.mda_timestamps,
            conversion=fl_mda.conversion,
            comments="No comment",
            description="Recording of extracellular voltage"
    )
