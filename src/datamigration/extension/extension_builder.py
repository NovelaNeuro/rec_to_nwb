import os

from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec, NWBDatasetSpec

path = os.path.dirname(os.path.abspath(__file__))


class ExtensionsBuilder:
    def __init__(self, ext_source, ns_path):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            doc="Extension for use in Novela Neurotechnologies",
            name="NovelaNeurotechnologies",
            version='1.0.0'
        )

        self.fl_electrode_group = self.create_fl_electrode_group()
        self.probes = self.create_probe()
        self.ntrode = self.create_ntrode()
        self.edge = self.create_edge()
        self.node = self.create_node()
        self.apparatus = self.create_apparatus()
        self.header_device = self.create_header_device()

        ns_builder.add_spec(self.ext_source, self.fl_electrode_group)
        ns_builder.add_spec(self.ext_source, self.probes)
        ns_builder.add_spec(self.ext_source, self.ntrode)
        ns_builder.add_spec(self.ext_source, self.apparatus)
        ns_builder.add_spec(self.ext_source, self.header_device)

        ns_builder.include_type('ElectrodeGroup', namespace='core')
        ns_builder.include_type('Device', namespace='core')
        ns_builder.include_type('NWBDataInterface', namespace='core')

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

    @staticmethod
    def create_node():
        """
            Node
            -----
            Abstract represention for any kind of node in the topological graph
            We won't actually implement abstract nodes. Rather this is a parent group
            from which our more specific types of nodes will inherit. Note that NWB
            specifications have inheritance.
            The quantity '*' means that we can have any number (0 or more) nodes.
        """
        return NWBGroupSpec(
            neurodata_type_def='Node',
            neurodata_type_inc='NWBDataInterface',
            doc='nodes in the graph',
            quantity='*',
            attributes=[NWBAttributeSpec(name='name',
                                         doc='the name of this node',
                                         dtype='text'),
                        NWBAttributeSpec(name='value',
                                         doc='the value of this node',
                                         dtype='int'),
                        NWBAttributeSpec(name='help',
                                         doc='help doc',
                                         dtype='text',
                                         value='Apparatus Node')])

    @staticmethod
    def create_edge():
        """
            Edge
            -------
            Edges between any two nodes in the graph.
            An edge's only dataset is the name (string) of the two nodes that the
            edge connects
            Note that we don't actually include the nodes themselves, just their
            names, in an edge.
        """
        return NWBGroupSpec(
            neurodata_type_def='Edge',
            neurodata_type_inc='NWBDataInterface',
            doc='edges in the graph',
            quantity='*',
            datasets=[
                NWBDatasetSpec(
                    doc='names of the nodes this edge connects',
                    name='edge_nodes',
                    dtype='text',
                    dims=['first_node_name|second_node_name'],
                    shape=[2])],
            attributes=[
                NWBAttributeSpec(
                    name='help',
                    doc='help doc',
                    dtype='text',
                    value='Apparatus Edge')])

    def create_apparatus(self):
        """
            Apparatus
            -------------
            Finally, we define the apparatus itself.
            It is has two sub-groups: nodes and edges.
        """
        return NWBGroupSpec(
            neurodata_type_def='Apparatus',
            neurodata_type_inc='NWBDataInterface',
            doc='a graph of nodes and edges',
            quantity='*',
            groups=[self.node, self.edge],
            attributes=[
                NWBAttributeSpec(name='name',
                                 doc='the name of this apparatus',
                                 dtype='text'),
                NWBAttributeSpec(name='help',
                                 doc='help doc',
                                 dtype='text',
                                 value='Behavioral Apparatus')])

    @staticmethod
    def create_header_device():
        return NWBGroupSpec(
            doc='metadata from global configuration from header',
            neurodata_type_def='HeaderDevice',
            neurodata_type_inc='Device',
            attributes=[
                NWBAttributeSpec(
                    name='headstage_serial',
                    doc='headstage_serial from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_smart_ref_on',
                    doc='headstage_smart_ref_on from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='realtime_mode',
                    doc='realtime_mode from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_auto_settle_on',
                    doc='headstage_auto_settle_on from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='timestamp_at_creation',
                    doc='timestamp_at_creation from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='controller_firmware_version',
                    doc='conntroller_firmware_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='controller_serial',
                    doc='controller_serial from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='save_displayed_chan_only',
                    doc='save_displayed_chan_only from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_firmware_version',
                    doc='headstage_firmware_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='qt_version',
                    doc='qt_version_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='compile_date',
                    doc='compile_date_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='compile_time',
                    doc='compile_time_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='file_prefixn',
                    doc='file_prefix_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_gyro_sensor_on',
                    doc='headstage_gyro_sensor_on_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_mag_sensor_on',
                    doc='headstage_mag_sensor_on_version from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='trodes_version',
                    doc='trodes_versionversion from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='headstage_accel_sensor_on',
                    doc='headstage_accel_sensor_on from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='commit_head',
                    doc='commit_head from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='system_time_at_creation',
                    doc='system_time_at_creation from global configuration',
                    dtype='text'
                ),
                NWBAttributeSpec(
                    name='file_path',
                    doc='file_path from global configuration',
                    dtype='text'
                ),
            ]
        )


build_extensions = ExtensionsBuilder('NovelaNeurotechnologies.specs.yaml', 'NovelaNeurotechnologies.namespace.yaml')

