from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec


class ExtensionsBuilder:
    def __init__(self, ext_source, ns_path):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            doc="Extension for use in Novela Neurotechnologies",
            name="NovelaNeurotechnologies"
        )

        self.electrodes = self.create_fl_electordes()
        self.shank = self.create_shank()
        self.probes = self.create_probe()

        ns_builder.add_spec(self.ext_source, self.electrodes)
        ns_builder.add_spec(self.ext_source, self.shank)
        ns_builder.add_spec(self.ext_source, self.probes)

        ns_builder.include_type('ElectrodeGroup', namespace='core')
        # ns_builder.include_type('ElectrodeTable', namespace='core')
        ns_builder.include_type('Device', namespace='core')

        ns_builder.export(self.ns_path)

    def create_fl_electordes(self):
        return NWBGroupSpec(
            'A custom Electrodes interface',
            neurodata_type_def='FLElectrodes',
            # neurodata_type_inc='ElectrodeTable',
            attributes=[
                # NWBAttributeSpec(
                #     name='id',
                #     doc='a unique identifier for the electrode',
                #     dtype='int'
                # ),
                NWBAttributeSpec(
                    name='maxDisp',
                    doc='maxDisp sample description',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='triggerOn',
                    doc='triggerOn sample description',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='hwChan',
                    doc='hwChan sample description',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='thresh',
                    doc='thresh sample description',
                    dtype='text'
                ),
            ],
        )

    def create_shank(self):
        return NWBGroupSpec(
            name='Shank default name',
            doc='A custom ElectrodesGroup interface',
            neurodata_type_def='Shank',
            neurodata_type_inc='ElectrodeGroup',
            attributes=[
                NWBAttributeSpec(
                    name='filterOn',
                    doc='filterOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='lowFilter',
                    doc='lowFilter sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='lfpRefOn',
                    doc='lfpRefOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='color',
                    doc='color sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='highFilter',
                    doc='highFilter sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='lfpFilterOn',
                    doc='lfpFilterOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='moduleDataOn',
                    doc='moduleDataOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='LFPHighFilter',
                    doc='LFPHighFilter sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='refGroup',
                    doc='refGroup sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='LFPChan',
                    doc='LFPChan sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='refNTrodeID',
                    doc='refNTrodeID sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='refChan',
                    doc='refChan sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='groupRefOn',
                    doc='groupRefOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='refOn',
                    doc='refOn sample doc',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='id',
                    doc='id sample doc',
                    dtype='text'
                ),

            ],
        )

    def create_probe(self):
        return NWBGroupSpec(
            'A custom Probes interface',
            neurodata_type_def='Probe',
            neurodata_type_inc='Device',
            attributes=[
                NWBAttributeSpec(
                    name='probe_id',
                    doc='unique id of the probe',
                    dtype='text'
                ),
            ]
        )
