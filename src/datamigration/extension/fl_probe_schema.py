from pynwb.spec import NWBNamespaceBuilder, NWBGroupSpec, NWBAttributeSpec

ns_path = "NovelaNeurotechnologies.namespace.yaml"
ext_source = 'NovelaNeurotechnologies.extensions.yaml'
ns_builder = NWBNamespaceBuilder('Extension for use in my Lab', "mylab")
ns_builder.include_type('Device', namespace='core')
ext = NWBGroupSpec('A custom Device for my lab',
                   attributes=[NWBAttributeSpec('Probe_name', 'the probe name', 'text')],
                   neurodata_type_inc='Device',
                   neurodata_type_def='Probe')
ns_builder.add_spec(ext_source, ext)
ns_builder.export(ns_path)
