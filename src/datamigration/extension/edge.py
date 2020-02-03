import logging.config
import os

from hdmf import docval
from pynwb import load_namespaces, register_class, NWBContainer

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)

path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@register_class('Edge',  'NovelaNeurotechnologies')
class Edge(NWBContainer):
    '''An undirected edge connecting two nodes in a graph.
    Attributes
    ----------
    name : str
    edge_nodes : iterable
        The names of the two Node objects connected by this edge (e.g.
        [node1 name, node2 name])
    '''

    __nwbfields__ = ('name', 'edge_nodes')

    @docval({'name': 'name', 'type': str, 'doc': 'name of this segement node'},
            {'name': 'edge_nodes', 'type': ('array_data', 'data'),
             'doc': 'the names of the two nodes in this undirected edge'})
    def __init__(self, **kwargs):
        super(Edge, self).__init__(name=kwargs['name'])
        self.edge_nodes = kwargs['edge_nodes']