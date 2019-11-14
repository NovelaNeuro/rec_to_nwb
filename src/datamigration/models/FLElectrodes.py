# ToDo HardCoded namespaces, it is ok?
from pynwb import load_namespaces, NWBContainer, register_class
from pynwb.core import MultiContainerInterface

ns_path = "novelaNeurotechnologies.namespace.yaml"
load_namespaces(ns_path)


@register_class('FLElectrodes', 'novelaNeurotechnologies')
class FLElectrodes(NWBContainer):
    __nwbfields__ = ('name', 'x', 'y', 'z', 'imp', 'location',
                     'filtering', 'group', 'id', 'maxDisp', 'triggerOn', 'hwChan', 'thresh')

    # @docval(
    #         {'name': 'name', 'type': str, 'doc': 'the name pf the electrode'},
    #         {'name': 'x', 'type': float, 'doc': 'the x coordinate of the position'},
    #         {'name': 'y', 'type': float, 'doc': 'the y coordinate of the position'},
    #         {'name': 'z', 'type': float, 'doc': 'the z coordinate of the position'},
    #         {'name': 'imp', 'type': float, 'doc': 'the impedance of the electrode'},
    #         {'name': 'location', 'type': str, 'doc': 'the location of electrode within the subject e.g. brain region'},
    #         {'name': 'filtering', 'type': str, 'doc': 'description of hardware filtering'},
    #         {'name': 'group', 'type': FLElectrodesGroup, 'doc': 'the ElectrodeGroup object to add to this NWBFile'},
    #         {'name': 'id', 'type': int, 'doc': 'a unique identifier for the electrode'},
    #         {'name': 'maxDisp', 'type': str, 'doc': 'maxDisp sample description'},
    #         {'name': 'triggerOn', 'type': str, 'doc': 'triggerOn sample description'},
    #         {'name': 'hwChan', 'type': str, 'doc': 'hwChan sample description'},
    #         {'name': 'thresh', 'type': str, 'doc': 'thresh sample description'}
    # )

    def __init__(self, **kwargs):
        super(FLElectrodes, self).__init__(name=kwargs['name'])
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.z = kwargs['z']
        self.imp = kwargs['imp']
        self.location = kwargs['location']
        self.filtering = kwargs['filtering']
        self.group = kwargs['group']
        self.id = kwargs['id']
        self.maxDisp = kwargs['maxDisp']
        self.triggerOn = kwargs['triggerOn']
        self.hwChan = kwargs['hwChan']
        self.thresh = kwargs['thresh']


@register_class('FLElectrodesContainer', 'novelaNeurotechnologies')
class FLElectrodesContainer(MultiContainerInterface):
    __clsconf__ = {
        'attr': 'electrodes',
        'type': FLElectrodes,
        'add': 'add_electrodes',
        'get': 'get_electrodes',
        'create': 'create_electrodes',
    }
