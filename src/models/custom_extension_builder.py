from hdmf.spec import RefSpec
from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec


def create_fl_electordes():
    return NWBGroupSpec('A custom Electrode interface',
                        attributes=[
                            NWBAttributeSpec(
                                name='x',
                                doc='the x coordinate of the position',
                                dtype='float'
                            ),
                            NWBAttributeSpec(
                                name='y',
                                doc='the y coordinate of the position',
                                dtype='float'
                            ),
                            NWBAttributeSpec(
                                name='z',
                                doc='the z coordinate of the position',
                                dtype='float'
                            ),
                            NWBAttributeSpec(
                                name='imp',
                                doc='the impedance of the electrode',
                                dtype='float'
                            ),
                            NWBAttributeSpec(
                                name='location',
                                doc='the location of electrode within the subject e.g. brain region',
                                dtype='text'
                            ),
                            NWBAttributeSpec(
                                name='filtering ',
                                doc='description of hardware filtering',
                                dtype='text'
                            ),
                            NWBAttributeSpec(
                                name='group',
                                doc='the ElectrodeGroup object to add to this NWBFile',
                                dtype=RefSpec(
                                    # ToDo check if "or" works
                                    # target_type='fl_ElectrodesGroup' or 'ElectrodesGroup',
                                    target_type='fl_ElectrodesGroup',
                                    reftype='object'
                                )
                            ),
                            NWBAttributeSpec(
                                name='id',
                                doc='a unique identifier for the electrode',
                                dtype='int'
                            ),
                        ],
                        neurodata_type_inc='Electrodes',
                        neurodata_type_def='fl_Electrodes'
                        )


def create_fl_electorde_group():
    return NWBGroupSpec('A custom ElectrodeGroup interface',
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
                                    target_type='Device',
                                    reftype='object'
                                )
                            ),
                            NWBAttributeSpec(
                                name='filterOn',
                                doc='filterOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='lowFilter',
                                doc='lowFilter sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='lfpRefOn',
                                doc='lfpRefOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='color',
                                doc='color sample doc',
                                dtype='text'
                            ),
                            NWBAttributeSpec(
                                name='highFilter',
                                doc='highFilter sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='lfpFilterOn',
                                doc='lfpFilterOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='moduleDataOn',
                                doc='moduleDataOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='LFPHighFilter',
                                doc='LFPHighFilter sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='refGroup',
                                doc='refGroup sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='LFPChan',
                                doc='LFPChan sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='refNTrodeID',
                                doc='refNTrodeID sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='refChan',
                                doc='refChan sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='groupRefOn',
                                doc='groupRefOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='refOn',
                                doc='refOn sample doc',
                                dtype='int'
                            ),
                            NWBAttributeSpec(
                                name='id',
                                doc='id sample doc',
                                dtype='int'
                            ),

                        ],
                        neurodata_type_inc='ElectrodeGroup',
                        neurodata_type_def='fl_ElectrodeGroup'
                        )


class CustomExtensionsBuilder:
    def __init__(self, ext_source='novelaNeurotechnologies.specs.yaml',
                 ns_path='novelaNeurotechnologies.namespace.yaml'):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            "Extension for use in Novela Neurotechnologies",
            "novelaNeurotechnologies"
        )

        ext_fl_electrodes = create_fl_electordes()
        ext_fl_electrode_group = create_fl_electorde_group()

        ns_builder.add_spec(self.ext_source, ext_fl_electrodes)
        ns_builder.add_spec(self.ext_source, ext_fl_electrode_group)

        ns_builder.export(self.ns_path)
