from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodesNtrodeExtensionCreator:
    @classmethod
    def create_electrodes_ntrode_extension(cls, metadata):
        validate_parameters_not_none(__name__, metadata)

        ntrodes_extension = []
        for ntrode in metadata:
            ntrodes_extension.extend([ntrode['ntrode_id']] * len(ntrode['map']))
        return ntrodes_extension
