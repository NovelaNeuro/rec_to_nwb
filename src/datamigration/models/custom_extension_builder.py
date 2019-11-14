from hdmf.spec import RefSpec
from pynwb.spec import NWBGroupSpec, NWBNamespaceBuilder, NWBAttributeSpec


class CustomExtensionsBuilder:
    def __init__(self, ext_source='novelaNeurotechnologies.specs.yaml',
                 ns_path='novelaNeurotechnologies.namespace.yaml'):
        self.ext_source = ext_source
        self.ns_path = ns_path

        ns_builder = NWBNamespaceBuilder(
            "Extension for use in Novela Neurotechnologies",
            "novelaNeurotechnologies"
        )

        self.electrodes = self.create_fl_electordes()
        self.electrodes_container = self.create_fl_electrodes_container()
        self.electrodes_group = self.create_fl_electordes_group()
        self.electrodes_group_container = self.create_fl_electordes_group_container()
        self.probes = self.create_fl_probes()

        ns_builder.add_spec(self.ext_source, self.probes)

        # ns_builder.add_spec(self.ext_source, self.electrodes)
        ns_builder.add_spec(self.ext_source, self.electrodes_container)
        # ns_builder.add_spec(self.ext_source, self.electrodes_group)
        ns_builder.add_spec(self.ext_source, self.electrodes_group_container)

        # ToDo change path to src/datamigration/models/
        ns_builder.export(self.ns_path)

    def create_fl_electordes(self):
        return NWBGroupSpec('A custom Electrodes interface',
                            # ToDo not found Electrode type
                            # neurodata_type_inc='Electrode',
                            neurodata_type_def='FLElectrodes',
                            attributes=[
                                NWBAttributeSpec(
                                    name='name',
                                    doc='the name pf the electrode',
                                    dtype='text'
                                ),
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
                                    name='filtering',
                                    doc='description of hardware filtering',
                                    dtype='text'
                                ),
                                NWBAttributeSpec(
                                    name='group',
                                    doc='the ElectrodesGroup object to add to this NWBFile',
                                    dtype=RefSpec(
                                        # ToDo check if "or" works
                                        # target_type='fl_ElectrodesGroup' or 'ElectrodesGroup',
                                        target_type='FLElectrodesGroup',
                                        reftype='object'
                                    )
                                ),
                                NWBAttributeSpec(
                                    name='id',
                                    doc='a unique identifier for the electrode',
                                    dtype='int'
                                ),
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

    def create_fl_electrodes_container(self):
        return NWBGroupSpec(neurodata_type_def='FLElectrodesContainer',
                            neurodata_type_inc='NWBDataInterface',
                            name='Electrodes container',
                            doc='A container of electrodes', quantity='?',
                            groups=[self.electrodes])

    def create_fl_electordes_group(self):
        return NWBGroupSpec('A custom ElectrodesGroup interface',
                            neurodata_type_inc='ElectrodeGroup',
                            neurodata_type_def='FLElectrodesGroup',
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
                                    # Link to Probe
                                    dtype=RefSpec(
                                        target_type='Device',
                                        reftype='object'
                                    )
                                ),
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

    def create_fl_electordes_group_container(self):
        return NWBGroupSpec(neurodata_type_def='FLElectrodesGroupContainer',
                            neurodata_type_inc='NWBDataInterface',
                            name='ElectrodesGroup container',
                            doc='A container of ElectrodesGroup', quantity='?',
                            groups=[self.electrodes_group])

    def create_fl_shanks(self):
        return NWBGroupSpec('A custom Shanks interface',
                            neurodata_type_def='FLShanks',
                            attributes=[
                                NWBAttributeSpec(
                                    name='name',
                                    doc='unique name of the shank',
                                    dtype='text'
                                ),
                                NWBAttributeSpec(
                                    name='electrodes',
                                    doc='the electrodes colection associated with the shank',
                                    dtype=RefSpec(
                                        target_type='electrodes',
                                        reftype='object'
                                    )
                                )
                                        ]
                            )

    def create_fl_probes(self):
        return NWBGroupSpec('A custom Probes interface',
                            neurodata_type_def='FLProbes',
                            attributes=[
                                NWBAttributeSpec(
                                    name='probe_id',
                                    doc='unique id of the probe',
                                    dtype='text'
                                ),
                                NWBAttributeSpec(
                                    name='shanks',
                                    doc='the shanks colection associated with the probe',
                                    dtype=RefSpec(
                                        target_type='FLShank',
                                        reftype='object'
                                    )
                                )
                                        ]
                            )
