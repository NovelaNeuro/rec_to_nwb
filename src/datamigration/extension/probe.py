import os

from hdmf.utils import docval, call_docval_func, get_docval
from pynwb import register_class, load_namespaces

from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('Probe', 'NovelaNeurotechnologies')
class Probe(ElectrodeGroup):
    __nwbfields__ = ('id', 'ntrodes', 'electrode_groups', 'num_shanks', 'contact_size', 'probe_type')

    @docval(*get_docval(ElectrodeGroup.__init__) + (
            {'name': 'id', 'type': 'int', 'doc': 'id of probe'},
            {'name': 'ntrodes', 'type': 'list', 'doc': 'ntrodes list'},
            {'name': 'electrode_groups', 'type': 'list', 'doc': 'list of electrode groups'},
            {'name': 'num_shanks', 'type': 'int', 'doc': 'number of shanks'},
            {'name': 'contact_size', 'type': 'float', 'doc': 'contact size value'},
            {'name': 'probe_type', 'type': 'str', 'doc': 'type of probe'},

    ))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'id'
                            if kwargs_item != 'ntrodes'
                            if kwargs_item != 'electrode_groups'
                            if kwargs_item != 'num_shanks'
                            if kwargs_item != 'contact_size'
                            if kwargs_item != 'probe_type'
                            })
        call_docval_func(super(Probe, self).__init__, kwargs)
        self.id = kwargs['id']
        self.ntrodes = kwargs['ntrodes']
        self.electrode_groups = kwargs['electrode_groups']
        self.num_shanks = kwargs['num_shanks']
        self.contact_size = kwargs['contact_size']
        self.probe_type = kwargs['probe_type']
