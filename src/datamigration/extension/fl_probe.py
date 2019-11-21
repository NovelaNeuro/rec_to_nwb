from pynwb import register_class, load_namespaces
from pynwb.device import Device
from hdmf.utils import docval, call_docval_func, getargs, get_docval
import os

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)
@register_class('Probe', 'mylab')
class Probe(Device):
    __nwbfields__ = ('Probe_name',)
    @docval(*get_docval(Device.__init__) + (
        {'name': 'Probe_name', 'type': 'str', 'doc': 'the probe name'},))
    def __init__(self, **kwargs):
        call_docval_func(super(Probe, self).__init__, kwargs)
        self.Probe_name = getargs('Probe_name', kwargs)