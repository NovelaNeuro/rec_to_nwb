from pynwb import load_namespaces, NWBContainer, register_class
from pynwb.core import MultiContainerInterface

ns_path = "novelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('FLShanks', 'novelaNeurotechnologies')
class FLShanks(NWBContainer):
    __nwbfields__ = ('name', 'electrodes')

    def __init__(self, **kwargs):
        super(FLShanks, self).__init__(name=kwargs['name'])
        self.electrodes = kwargs['electrodes']


@register_class('FLProbe', 'novelaNeurotechnologies')
class FLProbes(NWBContainer):
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
