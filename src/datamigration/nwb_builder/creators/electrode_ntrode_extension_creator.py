class ElectrodesNtrodeExtensionCreator:
    @classmethod
    def create_electrodes_ntrode_extension(cls, metadata):
        ntrodes_extension = []
        for ntrode in metadata:
            for _ in ntrode['map']:
                ntrodes_extension.append(ntrode['ntrode_id'])
        return ntrodes_extension
