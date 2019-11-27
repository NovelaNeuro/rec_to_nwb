import os

from hdmf import docval
from hdmf.utils import get_docval, call_docval_func
from pynwb import load_namespaces, register_class
from pynwb.ecephys import ElectrodeGroup

ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('Shank', 'NovelaNeurotechnologies')
class Shank(ElectrodeGroup):
    __nwbfields__ = (
        'filterOn', 'lowFilter', 'lfpRefOn', 'color', 'highFilter', 'lfpFilterOn', 'moduleDataOn', 'LFPHighFilter',
        'refGroup', 'LFPChan', 'refNTrodeID', 'refChan', 'groupRefOn', 'refOn', 'id'
    )

    @docval(*get_docval(ElectrodeGroup.__init__) + (
            {'name': 'filterOn', 'type': str, 'doc': 'the impedance of the electrode'},
            {'name': 'lowFilter', 'type': str, 'doc': 'the location of electrode within the subject e.g. brain region'},
            {'name': 'lfpRefOn', 'type': str, 'doc': 'description of hardware filtering'},
            {'name': 'color', 'type': str, 'doc': 'the ElectrodeGroup object to add to this NWBFile'},
            {'name': 'highFilter', 'type': str, 'doc': 'a unique identifier for the electrode'},
            {'name': 'lfpFilterOn', 'type': str, 'doc': 'maxDisp sample description'},
            {'name': 'moduleDataOn', 'type': str, 'doc': 'triggerOn sample description'},
            {'name': 'LFPHighFilter', 'type': str, 'doc': 'hwChan sample description'},
            {'name': 'refGroup', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'LFPChan', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'refNTrodeID', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'refChan', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'groupRefOn', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'refOn', 'type': str, 'doc': 'thresh sample description'},
            {'name': 'id', 'type': str, 'doc': 'thresh sample description'},
    ))
    def __init__(self, **kwargs):
        super().__init__(**{kwargs_item: kwargs[kwargs_item]
                            for kwargs_item in kwargs.copy()
                            if kwargs_item != 'filterOn'
                            if kwargs_item != 'lowFilter'
                            if kwargs_item != 'lfpRefOn'
                            if kwargs_item != 'color'
                            if kwargs_item != 'highFilter'
                            if kwargs_item != 'lfpFilterOn'
                            if kwargs_item != 'moduleDataOn'
                            if kwargs_item != 'LFPHighFilter'
                            if kwargs_item != 'refGroup'
                            if kwargs_item != 'LFPChan'
                            if kwargs_item != 'refNTrodeID'
                            if kwargs_item != 'refChan'
                            if kwargs_item != 'groupRefOn'
                            if kwargs_item != 'refOn'
                            if kwargs_item != 'id'
                            })
        call_docval_func(super(Shank, self).__init__, kwargs)
        self.filterOn = kwargs['filterOn']
        self.lowFilter = kwargs['lowFilter']
        self.lfpRefOn = kwargs['lfpRefOn']
        self.color = kwargs['color']
        self.highFilter = kwargs['highFilter']
        self.lfpFilterOn = kwargs['lfpFilterOn']
        self.moduleDataOn = kwargs['moduleDataOn']
        self.LFPHighFilter = kwargs['LFPHighFilter']
        self.refGroup = kwargs['refGroup']
        self.LFPChan = kwargs['LFPChan']
        self.refNTrodeID = kwargs['refNTrodeID']
        self.refChan = kwargs['refChan']
        self.groupRefOn = kwargs['groupRefOn']
        self.refOn = kwargs['refOn']
        self.id = kwargs['id']
