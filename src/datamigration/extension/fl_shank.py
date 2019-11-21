from pynwb import register_class, load_namespaces
from hdmf.utils import docval, call_docval_func, getargs, get_docval
import os

from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)
@register_class('Shank', 'mylab')
class Shank(ElectrodeGroup):
    __nwbfields__ = ('Shank_name',)
    @docval(*get_docval(ElectrodeGroup.__init__) + (
        {'name': 'Shank_name', 'type': 'str', 'doc': 'the shank name'},))
    def __init__(self, **kwargs):
        call_docval_func(super(Shank, self).__init__, kwargs)
        self.Shank_name = getargs('Shank_name', kwargs)