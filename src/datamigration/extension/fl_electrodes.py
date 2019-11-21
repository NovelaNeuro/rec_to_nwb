# import os
# from hdmf import docval
# from hdmf.utils import get_docval, call_docval_func
# from pynwb import load_namespaces, register_class
# from pynwb.file import ElectrodeTable
#
# ns_path = os.path.dirname(os.path.abspath(__file__)) + "/NovelaNeurotechnologies.namespace.yaml"
# load_namespaces(ns_path)
#
#
# @register_class('FLElectrodes', 'NovelaNeurotechnologies')
# class FLElectrodes(ElectrodeTable):
#     __nwbfields__ = ('maxDisp', 'triggerOn', 'hwChan', 'thresh')
#
#     @docval(*get_docval(ElectrodeTable.__init__) + (
#             # {'name': 'id', 'type': int, 'doc': 'a unique identifier for the electrode'},
#             {'name': 'maxDisp', 'type': str, 'doc': 'maxDisp sample description'},
#             {'name': 'triggerOn', 'type': str, 'doc': 'triggerOn sample description'},
#             {'name': 'hwChan', 'type': str, 'doc': 'hwChan sample description'},
#             {'name': 'thresh', 'type': str, 'doc': 'thresh sample description'}
#     ))
#     def __init__(self, **kwargs):
#         call_docval_func(super(FLElectrodes, self).__init__, kwargs)
#         # self.id = kwargs['id']
#         self.maxDisp = kwargs['maxDisp']
#         self.triggerOn = kwargs['triggerOn']
#         self.hwChan = kwargs['hwChan']
#         self.thresh = kwargs['thresh']
