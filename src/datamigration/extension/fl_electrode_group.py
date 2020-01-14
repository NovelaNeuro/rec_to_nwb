import os

from hdmf import docval
from hdmf.utils import get_docval, call_docval_func
from pynwb import load_namespaces, register_class
from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('FLElectrodeGroup', 'NovelaNeurotechnologies')
class FLElectrodeGroup(ElectrodeGroup):
    __nwbfields__ = ('id', 'probe_id')

    @docval(*get_docval(ElectrodeGroup.__init__) + (
            {'name': 'id', 'type': 'int', 'doc': 'id or electrode group'},
            {'name': 'probe_id', 'type': 'int', 'doc': 'id of probe EG belongs to'},
            ))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'id'
                            if kwargs_item != 'probe_id'
                            })
        call_docval_func(super(FLElectrodeGroup, self).__init__, kwargs)
        self.id = kwargs['id']
        self.probe_id = kwargs['probe_id']
