from hdmf.spec import RefSpec
from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec

ns_builder = NWBNamespaceBuilder("Extension for use in Novela Neurotechnologies", "novelaNeurotechnologies")

ext1 = NWBGroupSpec('A custom ElectrodeGroup interface',
                    attributes=[
                        NWBAttributeSpec(
                            name='name',
                            doc='the name of this electrode',
                            dtype='text'
                        ),
                        NWBAttributeSpec(
                            name='description',
                            doc='description of this electrode group',
                            dtype='text'
                        ),
                        NWBAttributeSpec(
                            name='location',
                            doc='description of location of this electrode group',
                            dtype='text'
                        ),
                        NWBAttributeSpec(
                            name='device',
                            doc='the device that was used to record from this electrode group',
                            dtype=RefSpec(
                                target_type='GroupSpec',
                                reftype='object'
                            )
                        ),
                    ],
                    # datasets=[...],
                    # groups=[...],
                    neurodata_type_inc='ElectrodeGroup',
                    neurodata_type_def='fl_ElectrodeGroup')

ext_source = 'novelaNeurotechnologies.specs.yaml'
ns_builder.add_spec(ext_source, ext1)

ns_builder.include_namespace('novelaNeurotechnologies')

ns_path = 'novelaNeurotechnologies.namespace.yaml'
ns_builder.export(ns_path)
