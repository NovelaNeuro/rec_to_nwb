from fl.datamigration.tools.validate_parameters import validate_parameters_not_none


class ElectrodesNtrodeExtensionCreator:

    @classmethod
    def create_electrodes_ntrode_extension_ntrode_id(cls, metadata):
        validate_parameters_not_none(__name__, metadata)

        electrodes_ntrode_extension_ntrode_id = []
        for ntrode in metadata:
            electrodes_ntrode_extension_ntrode_id.extend([ntrode['ntrode_id']] * len(ntrode['map']))
        return electrodes_ntrode_extension_ntrode_id

    @classmethod
    def create_electrodes_ntrode_extension_bad_channels(cls, metadata):
        validate_parameters_not_none(__name__, metadata)

        electrodes_ntrode_extension_bad_channels = []
        for ntrode in metadata:
            electrodes_ntrode_extension_bad_channels.extend([True if counter in ntrode['bad_channels'] else False
                                                             for counter, _ in enumerate(ntrode['map'])])
        return electrodes_ntrode_extension_bad_channels
