import logging.config
import os

from hdmf.utils import docval, call_docval_func, get_docval
from pynwb import register_class, load_namespaces
from pynwb.device import Device

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)
path = os.path.dirname(os.path.abspath(__file__))

logging.config.fileConfig(fname=str(path) + '/../../logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)


@register_class('Probe', 'NovelaNeurotechnologies')
class Probe(Device):
    __nwbfields__ = ('id', 'contact_size', 'probe_type', 'num_shanks')

    @docval(*get_docval(Device.__init__) + (
            {'name': 'id', 'type': 'int', 'doc': 'unique id of the probe'},
            {'name': 'contact_size', 'type': 'float', 'doc': 'value of contact size as float'},
            {'name': 'probe_type', 'type': 'str', 'doc': 'type of probe'},
            {'name': 'num_shanks', 'type': 'int', 'doc': 'number of shanks associated with probe'}))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'probe_type'
                            if kwargs_item != 'id'
                            if kwargs_item != 'contact_size'
                            if kwargs_item != 'num_shanks'
                            })
        call_docval_func(super(Probe, self).__init__, kwargs)
        self.id = kwargs['id']
        self.probe_type = kwargs['probe_type']
        self.contact_size = kwargs['contact_size']
        self.num_shanks = kwargs['num_shanks']
