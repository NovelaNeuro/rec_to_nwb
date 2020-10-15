from rec_to_nwb.processing.nwb.components.analog.fl_analog import FlAnalog


class OldFlAnalogBuilder:

    @staticmethod
    def build(data, timestamps, description):
        return FlAnalog(data, timestamps, description)
