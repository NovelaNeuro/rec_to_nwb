import os

from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec, NWBDatasetSpec

path = os.path.dirname(os.path.abspath(__file__))


class ExtensionsBuilder:
    def __init__(self, ext_source, ns_path):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            doc="Extension for use in Novela Neurotechnologies",
            name="NovelaNeurotechnologies"
        )

        self.fl_electrode_group = self.create_fl_electrode_group()
        self.probes = self.create_probe()
        self.ntrode = self.create_ntrode()

        ns_builder.add_spec(self.ext_source, self.fl_electrode_group)
        ns_builder.add_spec(self.ext_source, self.probes)
        ns_builder.add_spec(self.ext_source, self.ntrode)

        ns_builder.include_type('ElectrodeGroup', namespace='core')
        ns_builder.include_type('Device', namespace='core')

        ns_builder.export(path=self.ns_path, outdir=path)

    @staticmethod
    def create_fl_electrode_group():
        return NWBGroupSpec(
            doc='A custom ElectrodesGroup interface',
            neurodata_type_def='FLElectrodeGroup',
            neurodata_type_inc='ElectrodeGroup',
            attributes=[
                            NWBAttributeSpec(
                                name='id',
                                doc='id of electrode group',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='probe_id',
                                doc='id of probe',
                                dtype='int'
                            ),

                        ],
        )

    @staticmethod
    def create_ntrode():
        return NWBGroupSpec(
            doc='A custom ntrode ElectrodesGroup interface',
            neurodata_type_def='NTrode',
            neurodata_type_inc='ElectrodeGroup',
            datasets=[
                NWBDatasetSpec(
                    doc='map of ntrodes',
                    name='map',
                    dtype='int',
                    dims=[2],
                    shape=[32])],
            attributes=[
                NWBAttributeSpec(
                    name='ntrode_id',
                    doc='id of electrode group',
                    dtype='int'
                ),
                NWBAttributeSpec(
                    name='probe_id',
                    doc='id of probe',
                    dtype='int'
                ),

            ],
        )

    @staticmethod
    def create_probe():
        return NWBGroupSpec(
            doc='A custom Probes interface',
            neurodata_type_def='Probe',
            neurodata_type_inc='Device',
            attributes=[
                NWBAttributeSpec(
                    name='id',
                    doc='unique id of the probe',
                    dtype='int'
                ),
                NWBAttributeSpec(
                    name='contact_size',
                    doc='value of contact size in float',
                    dtype='float'
                ),
                NWBAttributeSpec(
                    name='probe_type',
                    doc='type of the probe',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='num_shanks',
                    doc='number of shanks in probe',
                    dtype='int'
                ),
            ]
        )


build_extensions = ExtensionsBuilder('NovelaNeurotechnologies.specs.yaml', 'NovelaNeurotechnologies.namespace.yaml')
