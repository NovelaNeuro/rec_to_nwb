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

        self.probes = self.create_probe()

        ns_builder.add_spec(self.ext_source, self.probes)

        ns_builder.include_type('Device', namespace='core')

        ns_builder.export(path=self.ns_path, outdir=path)

    @staticmethod
    def create_probe():
        return NWBGroupSpec(
            doc='A custom Probes interface',
            neurodata_type_def='Probe',
            neurodata_type_inc='Device',
            attributes=[
                NWBAttributeSpec(
                    name='device_name',
                    doc='name of the device',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='probe_description',
                    doc='description of the probe',
                    dtype='text'
                ),
            ]
        )
