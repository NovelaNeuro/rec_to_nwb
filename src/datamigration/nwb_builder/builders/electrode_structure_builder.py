class ElectrodeStructureBuilder:  # todo rething this class || make this singleton
    def __init__(self, header, metadata):
        self.header = header
        self.metadata = metadata

    def build(self, nwb_content):
        """
            For each electrode group in metadata.yml, check if probe exist.
            If not create one.
            Create electrode_group
            Create electrodes from corresponding probe_type in probe.yml
        """

        probes = []
        electrode_groups = []
        for probe_counter, electrode_group_metadata in enumerate(self.metadata['electrode groups']):
            probe_metadata = self.probe_extractor.filtr_by_type(electrode_group_metadata['device_type'])

            electrode_group = self.electrodes_group_builder.create_electrode_group(electrode_group_metadata,
                                                                                   probe)  # todo build electrode groups in separate place as well as injecting into nwb
            electrode_groups.append(electrode_group)
            # ElectrodeGroupInjector(nwb_content).join_electrode_group(electrode_group)
            data_for_electrodes.appends(probe_metadata)
            self.electrodes_builder.build(probe_metadata, nwb_content, electrode_group)
