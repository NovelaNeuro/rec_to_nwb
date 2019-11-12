from pynwb.spec import NWBDatasetSpec, NWBNamespaceBuilder, NWBAttributeSpec

# create a builder for the namespace
probe_builder = NWBNamespaceBuilder("Extension for storage probe information", "probe")

# create extensions
probe = NWBDatasetSpec('A custom NWB probe',
                    name='probe',
                    attribute=[
                        NWBAttributeSpec('probe_prop', 'a value for pp', 'str'),
                    ],
                    shape=(None, None))

# add the extension
ext_source = 'my_novela_lab_specs.yaml'
probe_builder.add_spec(ext_source, probe)


# save the namespace and extensions
ns_path = 'my_novela_lab.namespace.yaml'
probe_builder.export(ns_path)