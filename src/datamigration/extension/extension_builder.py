import os

from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec

path = os.path.dirname(os.path.abspath(__file__))

class ExtensionsBuilder:
    def __init__(self, ext_source, ns_path):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            doc="Extension for use in Novela Neurotechnologies",
            name="NovelaNeurotechnologies"
        )

        self.shank = self.create_shank()
        self.probes = self.create_probe()

        ns_builder.add_spec(self.ext_source, self.shank)
        ns_builder.add_spec(self.ext_source, self.probes)

        ns_builder.include_type('ElectrodeGroup', namespace='core')
        ns_builder.include_type('Device', namespace='core')

        ns_builder.export(path=self.ns_path, outdir=path)

    def create_shank(self):
        return NWBGroupSpec(
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
            doc='A custom Probes interface',
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
