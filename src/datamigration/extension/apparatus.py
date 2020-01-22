import os

from pynwb import load_namespaces, register_class
from pynwb.core import MultiContainerInterface

from src.datamigration.extension.edge import Edge
from src.datamigration.extension.node import Node

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('Apparatus', 'NovelaNeurotechnologies')
class Apparatus(MultiContainerInterface):
    """Topological graph representing connected components of a behavioral
    apparatus.
    Attributes
    ----------
    name : str
    nodes : list
        Node objects contained in this apparatus
    edges : list
        Edge objects contained in this apparatus
    """

    __nwbfields__ = ('name', 'edges', 'nodes')

    __clsconf__ = [
        {
            'attr': 'edges',
            'type': Edge,
            'add': 'add_edge',
            'get': 'get_edge'
        },
        {
            'attr': 'nodes',
            'type': Node,
            'add': 'add_node',
            'get': 'get_node'
        }
    ]
    __help = 'info about an apparatus.py'