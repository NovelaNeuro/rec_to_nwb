class ElectrodesNtrodeExtensionCreator:
    @classmethod
    def create_electrodes_ntrode_extension(cls, metadata):
        ntrodes_extension = []
        for ntrode in metadata:
            ntrodes_extension.extend([ntrode['ntrode_id']] * len(ntrode['map']))
        return ntrodes_extension
