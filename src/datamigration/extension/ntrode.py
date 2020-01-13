import os

from hdmf import docval
from hdmf.utils import get_docval, call_docval_func
from pynwb import load_namespaces, register_class
from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('FLElectrodeGroup', 'NovelaNeurotechnologies')
class NTrode(ElectrodeGroup):
    __nwbfields__ = ('ntrode_id', 'probe_id', 'map')

    @docval(*get_docval(ElectrodeGroup.__init__) + (
            {'name': 'ntrode_id', 'type': 'int', 'doc': 'id of electrode group'},
            {'name': 'probe_id', 'type': 'int', 'doc': 'id of probe EG belongs to'},
            {'name': 'map', 'type': 'array_data', 'doc': 'map of ntrode'},
            ))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'ntrode_id'
                            if kwargs_item != 'probe_id'
                            if kwargs_item != 'map'
                            })
        call_docval_func(super(NTrode, self).__init__, kwargs)
        self.ntrode_id = kwargs['ntrode_id']
        self.probe_id = kwargs['probe_id']
        self.map = kwargs['map']
