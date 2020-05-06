from fldatamigration.processing.nwb.components.analog.fl_analog import FlAnalog


class FlAnalogBuilder:

    @staticmethod
    def build(data, timestamps):
        return FlAnalog(data, timestamps)