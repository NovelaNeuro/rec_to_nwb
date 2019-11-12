from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec

ns_path = "mylab.namespace.yaml"
ext_source = "mylab.extensions.yaml"

ns_builder = NWBNamespaceBuilder('Extension for novela', "novela")

ns_builder.include_type('ElectricalSeries', namespace='core')

ext = NWBGroupSpec('a probe for novela',
                   attributes=[NWBAttributeSpec('probe_id', 'the probe id', 'int'), NWBAttributeSpec('probe2_id', 'the probe2 id', 'int')],
                   neurodata_type_inc='ElectricalSeries',
                   neurodata_type_def='ProbeSeries')

ns_builder.add_spec(ext_source, ext)
ns_builder.export(ns_path)
