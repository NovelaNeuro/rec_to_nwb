from pynwb import load_namespaces, register_class
from pynwb.core import MultiContainerInterface
from pynwb.device import Device
from pynwb.ecephys import ElectrodeGroup

ns_path = "novelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('FLShanks', 'novelaNeurotechnologies')
class FLShanks(ElectrodeGroup):
    __nwbfields__ = ('name', 'electrodes')

    def __init__(self, **kwargs):
        super(FLShanks, self).__init__(name=kwargs['name'])
        self.electrodes = kwargs['electrodes']


@register_class('FLProbe', 'novelaNeurotechnologies')
class FLProbes(Device):
    __nwbfields__ = ('probe_id', 'shanks')

    def __init__(self, **kwargs):
        super(FLProbes, self).__init__(name=kwargs['probe_id'])
        self.shanks = kwargs['shanks']


@register_class('FLProbesContainer', 'novelaNeurotechnologies')
class FLProbesContainer(MultiContainerInterface):
    __clsconf__ = {
        'attr': 'Probe',
        'type': FLProbes,
        'add': 'add_Probe',
        'get': 'get_Probe',
        'create': 'create_Probe',
    }
