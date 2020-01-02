import os

from hdmf.utils import docval, call_docval_func, get_docval
from pynwb import register_class, load_namespaces
from pynwb.device import Device

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('Probe', 'NovelaNeurotechnologies')
class Probe(Device):
    __nwbfields__ = ('probe_id', 'probe_type', 'probe_description')

    @docval(*get_docval(Device.__init__) + (
            {'name': 'probe_id', 'type': 'str', 'doc': 'unique id of the probe'},
            {'name': 'probe_type', 'type': 'str', 'doc': 'type of the probe'},
            {'name': 'probe_description', 'type': 'str', 'doc': 'description of the probe'},
    ))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'probe_id'
                            if kwargs_item != 'probe_type'
                            if kwargs_item != 'probe_description'
                            })
        call_docval_func(super(Probe, self).__init__, kwargs)
        self.probe_id = kwargs['probe_id']
        self.probe_type = kwargs['probe_type']
        self.probe_description = kwargs['probe_description']
