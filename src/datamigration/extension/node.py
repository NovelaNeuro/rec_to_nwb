import os

from hdmf import docval
from hdmf.utils import get_docval, call_docval_func
from pynwb import load_namespaces, register_class, NWBContainer
from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('Node', 'NovelaNeurotechnologies')
class Node(NWBContainer):
    '''A generic graph node. Subclass for more specific types of nodes.
    Attributes
    ----------
    name : str
    value: int
    '''

    __nwbfields__ = ('name',)

    @docval({'name': 'name', 'type': str, 'doc': 'name of this node'},
            {'name': 'value', 'type': int, 'doc': 'value of this node'})
    def __init__(self, **kwargs):
        super(Node, self).__init__(name=kwargs['name'])
        self.value = kwargs['value']
