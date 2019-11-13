import os

from pynwb import load_namespaces, NWBContainer, register_class
from pynwb.core import MultiContainerInterface

ns_path = "novelaNeurotechnologies.namespace.yaml"
try:
    load_namespaces(ns_path)
except:
    print(os.getcwd()
          )


@register_class('FLElectrodesGroup', 'novelaNeurotechnologies')
class FLElectrodesGroup(NWBContainer):
    __nwbfields__ = ('name', 'description', 'location', 'device', 'filterOn', 'lowFilter',
                     'lfpRefOn', 'color', 'highFilter', 'lfpFilterOn', 'moduleDataOn', 'LFPHighFilter', 'refGroup'
                                                                                                        'LFPChan',
                     'refNTrodeID', 'refChan', 'groupRefOn', 'refOn', 'id'
                     )

    # @docval(*get_docval(NWBContainer.__init__) + (
    #         {'name': 'name', 'type': str, 'doc': 'the name pf the electrode'},
    #         {'name': 'description', 'type': str, 'doc': 'the x coordinate of the position'},
    #         {'name': 'location', 'type': str, 'doc': 'the y coordinate of the position'},
    #         {'name': 'device', 'type': Device, 'doc': 'the z coordinate of the position'},
    #         {'name': 'filterOn', 'type': str, 'doc': 'the impedance of the electrode'},
    #         {'name': 'lowFilter', 'type': str, 'doc': 'the location of electrode within the subject e.g. brain region'},
    #         {'name': 'lfpRefOn', 'type': str, 'doc': 'description of hardware filtering'},
    #         {'name': 'color', 'type': str, 'doc': 'the ElectrodeGroup object to add to this NWBFile'},
    #         {'name': 'highFilter', 'type': str, 'doc': 'a unique identifier for the electrode'},
    #         {'name': 'lfpFilterOn', 'type': str, 'doc': 'maxDisp sample description'},
    #         {'name': 'moduleDataOn', 'type': str, 'doc': 'triggerOn sample description'},
    #         {'name': 'LFPHighFilter', 'type': str, 'doc': 'hwChan sample description'},
    #         {'name': 'refGroup', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'LFPChan', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'refNTrodeID', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'refChan', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'groupRefOn', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'refOn', 'type': str, 'doc': 'thresh sample description'},
    #         {'name': 'id', 'type': str, 'doc': 'thresh sample description'},
    # ))
    def __init__(self, **kwargs):
        super(FLElectrodesGroup, self).__init__(name=kwargs['name'])
        self.description = kwargs['description']
        self.location = kwargs['location']
        self.device = kwargs['device']
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


@register_class('FLElectrodesGroupContainer', 'novelaNeurotechnologies')
class FLElectrodesGroupContainer(MultiContainerInterface):
    __clsconf__ = {
        'attr': 'electrodes_group',
        'type': FLElectrodesGroup,
        'add': 'add_electrodes_group',
        'get': 'get_electrodes_group',
        'create': 'create_electrodes_group',
    }
