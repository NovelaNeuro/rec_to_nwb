from src.datamigration.tools.validate_input_parameters import validate_input_parameters


class ElectrodesNtrodeExtensionCreator:
    @classmethod
    def create_electrodes_ntrode_extension(cls, metadata):
        validate_input_parameters(__name__, metadata)

        ntrodes_extension = []
        for ntrode in metadata:
            ntrodes_extension.extend([ntrode['ntrode_id']] * len(ntrode['map']))
        return ntrodes_extension
