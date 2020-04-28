from fl.datamigration.nwb.components.electrodes.extension.fl_electrode_extension_factory import \
    FlElectrodeExtensionFactory


class BadDataManager:

    def __init__(self, metadata):
        self.metadata = metadata

    def get_valid_map_dict(self):

        electrodes_valid_map = self.__get_electrodes_valid_map(
            ntrode_metadata=self.metadata['ntrode electrode group channel map']
        )
        electrode_groups_valid_map = self.__get_electrode_groups_valid_map(

        )
        probes_valid_map = self.__get_probes_valid_map(

        )
        # ToDo validate()

        return {
            'electrodes': electrodes_valid_map,
            'electrode_group': electrode_groups_valid_map,
            'probes': probes_valid_map,
        }

    @staticmethod
    def __get_electrodes_valid_map(ntrode_metadata):
        return FlElectrodeExtensionFactory.create_bad_channels(
            ntrode_metadata=ntrode_metadata
        )

    def __get_electrode_groups_valid_map(self):
        pass

    def __get_probes_valid_map(self):
        pass